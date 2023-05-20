from . import utils


# scene objects chunks
CHUNK_SCENE_OBJECTS = 0x8002

# tools chunk
TOOLS_CHUNK_OBJECTS = 0x3
TOOLS_CHUNK_OBJECT_DATA = 0x7777

# object chunks
EOBJ_CHUNK_REFERENCE = 0x0902


def read_object_data(data, objects_list):
    chunked_reader = xray.reader.ChunkedReader(data)

    for chunk_id, chunk_data in chunked_reader:
        if chunk_id == EOBJ_CHUNK_REFERENCE:
            packed_reader = xray.reader.PackedReader(chunk_data)
            packed_reader.skip(8)    # "<2I" file_version and unknown
            reference = packed_reader.gets()
            objects_list.add(reference)


def read_object(data, objects_list):
    object_reader = xray.reader.ChunkedReader(data)

    for chunk_id, chunk_data in object_reader:
        if chunk_id == TOOLS_CHUNK_OBJECT_DATA:
            read_object_data(chunk_data, objects_list)


def read_objects(data, objects_list):
    objects_reader = xray.reader.ChunkedReader(data)

    for object_id, object_data in objects_reader:
        read_object(object_data, objects_list)


def read_scene_objects(data, objects_list):
    chunked_reader = xray.reader.ChunkedReader(data)

    for chunk_id, chunk_data in chunked_reader:
        if chunk_id == TOOLS_CHUNK_OBJECTS:
            read_objects(chunk_data, objects_list)


def read_scene_objects_part(file_path, objects_list):
    # scene_objects.part for soc

    data = utils.read_file(file_path)

    chunked_reader = xray.reader.ChunkedReader(data)
    for chunk_id, chunk_data in chunked_reader:

        if chunk_id == CHUNK_SCENE_OBJECTS:
            references = read_scene_objects(chunk_data, objects_list)
