from typing import Tuple, Dict
from enum import Enum
import os
import struct

PAGE_SIZE = 4096

class Pager():
    fd : int
    def __init__(self, filename : str):
        self.fd = os.open(filename, os.O_RDWR | os.O_CREAT)
    def read_page(self, page : int):
        return os.pread(self.fd, PAGE_SIZE, page * PAGE_SIZE)
    def page_amount(self) -> int:
        return os.fstat(self.fd).st_size // PAGE_SIZE
    def new_page(self) -> int:
        pages = self.page_amount()
        os.ftruncate(self.fd, (pages + 1) * PAGE_SIZE)
        return pages
    def write_page(self, page : int, buf : bytes):
        os.pwritev(self.fd, [buf], PAGE_SIZE * page)

MAX_SCHEMAS = (PAGE_SIZE - 36) // 4

class Header():
    version : int
    db_name : str
    schemas : list[int]
    def from_buffer(buf : bytes):
        h = Header()
        a = struct.unpack("<H32pH"+str(MAX_SCHEMAS)+"I", buf)
        h.version = a[0]
        h.db_name = a[1].decode("utf-8")
        h.schemas = list(a[3:(3+a[2])])
        return h
    def to_buffer(self) -> bytes:
        top = struct.pack("<H32pH"
                , self.version
                , bytes(self.db_name, "utf-8")
                , len(self.schemas))
        bottom = bytes(0)
        for schema in self.schemas:
            bottom += schema.to_bytes(4, "little")
        bottom += bytes((MAX_SCHEMAS - len(self.schemas))*4)
        return top + bottom


class Datatype(Enum):
    INT = 0
    BOOL = 1
    STR = 2 # 32 byte pascal string
    def size(self):
        if self.value == 0:
            return 4
        if self.value == 1:
            return 1
        if self.value == 2:
            return 32
    def from_bytes(self, buf):
        if self.value == 0:
            return int.from_bytes(buf, "little")
        if self.value == 1:
            return int.from_bytes(buf, "little") != 0
        if self.value == 2:
            return struct.unpack("<32p", buf)[0].decode("utf-8")
    def to_bytes(self, value):
        if self.value == 0:
            return value.to_bytes(4, "little")
        if self.value == 1:
            return int(value).to_bytes(1, "little")
        if self.value == 2:
            return struct.pack("<32p", bytes(value, "utf-8"))
    def __repr__(self):
        if self.value == 0:
            return "INTEGER"
        if self.value == 1:
            return "BOOLEAN"
        if self.value == 2:
            return "STRING"


MAX_FIELDS = (PAGE_SIZE - 41) // 33

class SchemaPage():
    name : str
    first_storage_page : int
    last_storage_page : int # unused TODO: use it
    fields : list[Tuple[str, Datatype]] # str 32 byte pascal string, Datatype 1 byte
    def __init__(self):
        self.name = ""
        self.first_storage_page = 0
        self.last_storage_page = 0
        self.fields = []
    def from_buffer(buf : bytes):
        sp = SchemaPage()
        a = struct.unpack("<32pIIB", buf[:41])
        sp.name = a[0].decode("utf-8")
        sp.first_storage_page = a[1]
        sp.last_storage_page = a[2]
        sp.fields = []
        field_amount = a[3] 
        for x in range(0, field_amount):
            x *= 33
            x += 41
            a = struct.unpack("<32pB", buf[x:x+33])
            sp.fields.append((a[0].decode("utf-8"), Datatype(a[1])))
        return sp
    def to_buffer(self) -> bytes:
        top = struct.pack("<32pIIB"
                , bytes(self.name, "utf-8")
                , self.first_storage_page
                , self.last_storage_page
                , len(self.fields))
        bottom = bytes(0)
        for field in self.fields:
            bottom += struct.pack("<32p", bytes(field[0], "utf-8"))
            bottom += field[1].value.to_bytes(1, "little")
        bottom += bytes((MAX_FIELDS - len(self.fields)) * 33)
        return top + bottom

class StoragePage():
    next_page : int
    _schema : list[Datatype]
    MAX_ROWS : int
    ROW_SIZE : int
    values : list[Tuple]
    def __init__(self, schema : list[Datatype] = None):
        self.next_page = 0
        self.values = []
        if schema != None:
            self.ROW_SIZE = sum([x.size() for x in schema])
            self.MAX_ROWS = (PAGE_SIZE - 4) // self.ROW_SIZE
            self._schema = schema

    def from_buffer(buf : bytes, schema : list[Datatype]):
        stp = StoragePage(schema)
        stp.next_page = int.from_bytes(buf[:4], "little")
        row_amount = int.from_bytes(buf[4:6], "little")
        for x in range(0, row_amount):
            x *= stp.ROW_SIZE
            x += 6
            ret = []
            for typ in stp._schema:
                ret.append(typ.from_bytes(buf[x:x+typ.size()]))
                x += typ.size()
            stp.values.append(tuple(ret))
        return stp
    def to_buffer(self) -> bytes:
        top = self.next_page.to_bytes(4, "little") + len(self.values).to_bytes(2, "little")
        bottom = bytes(0)
        for value in self.values:
            if len(value) != len(self._schema):
                raise Exception("Got to many items in row!")
            for typ, item in zip(self._schema, value):
                bottom += typ.to_bytes(item)
        bottom += bytes((self.MAX_ROWS - len(self.values)) * self.ROW_SIZE)
        return top + bottom

VERSION = 1

class DB():
    pager : Pager
    #{"users" : 
    #    (["id", "name", "password"],               # names
    #    [Datatype.INT, Datatype.STR, Datatype.STR],# types
    #    12,                                        # first storage page
    #    2)}                                        # schema page
    _schemas : Dict[str, Tuple[list[str], list[Datatype], int, int]]
    def __init__(self, filename : str):
        self.pager = Pager(filename)
        self._schemas = {}
        if self.pager.page_amount() == 0:
            h = Header.from_buffer(self.pager.read_page(newpage := self.pager.new_page()))
            h.version = VERSION
            h.db_name = "TODO: use name of file"
            self.pager.write_page(newpage, h.to_buffer())
        else:
            h = Header.from_buffer(self.pager.read_page(0))
            for schema in h.schemas:
                sp = SchemaPage.from_buffer(self.pager.read_page(schema))
                names = []
                types = []
                for name, typ in sp.fields:
                    names.append(name)
                    types.append(typ)
                self._schemas[sp.name] = (names, types, sp.first_storage_page, schema)
    def add_table(self, name : str, schema : list[Tuple[str, Datatype]]):
        if name in self._schemas:
            raise Exception("Table already exists")
        h = Header.from_buffer(self.pager.read_page(0))
        newpage = self.pager.new_page()
        h.schemas.append(newpage)
        self.pager.write_page(0, h.to_buffer())
        sp = SchemaPage()
        sp.name = name
        sp.fields = schema
        self.pager.write_page(newpage, sp.to_buffer())
        names = []
        types = []
        for name, typ in sp.fields:
            names.append(name)
            types.append(typ)
        self._schemas[sp.name] = (names, types, 0, newpage)
    def insert(self, table : str, row : tuple):
        schema = list(zip(self._schemas[table][0], self._schemas[table][1]))
        schema_typ = self._schemas[table][1]
        storagepage = self._schemas[table][2]
        # if no sp exists create one
        if storagepage == 0:
            stp = StoragePage(schema_typ)
            stp.values.append(row)
            self.pager.write_page(newpage := self.pager.new_page(), stp.to_buffer())
            schemapage = self._schemas[table][3]
            sp = SchemaPage.from_buffer(self.pager.read_page(schemapage))
            sp.first_storage_page = newpage
            self.pager.write_page(schemapage, sp.to_buffer())
            nse = list(self._schemas[table])
            nse[2] = newpage
            self._schemas[table] = tuple(nse)
            return
        storage = StoragePage.from_buffer(self.pager.read_page(storagepage), schema_typ)
        # goto newest page
        while storage.next_page != 0:
            storage = StoragePage.from_buffer(self.pager.read_page(storagepage := storage.next_page), schema_typ)
        # create new page if it is full
        if len(storage.values) == storage.MAX_ROWS:
            newpage = self.pager.new_page()
            storage.next_page = newpage
            self.pager.write_page(storagepage, storage.to_buffer())
            storage = StoragePage.from_buffer(self.pager.read_page(storagepage := newpage), schema_typ)
        storage.values.append(row)
        self.pager.write_page(storagepage, storage.to_buffer())
    def seq_reader(self, table : str):
        schema_typ = self._schemas[table][1]
        storagepage = self._schemas[table][2]
        while storagepage != 0:
            stp = StoragePage.from_buffer(self.pager.read_page(storagepage), schema_typ)
            for value in stp.values:
                yield value
            storagepage = stp.next_page
