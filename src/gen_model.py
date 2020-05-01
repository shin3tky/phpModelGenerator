import sys
import xml.etree.ElementTree as ET


def generate_converter_method(table):
    table_name = table.attrib["name"]
    print(
        "    public function to"
        + to_pascal_case(table_name)
        + "(ORM $item) : "
        + to_pascal_case(table_name)
        + " {"
    )
    print(
        "        $"
        + to_camel_case(table_name)
        + " = new "
        + to_pascal_case(table_name)
        + "();"
    )

    for field in table.findall("./field"):
        field_name = field.attrib["Field"]
        print(
            "        $"
            + to_camel_case(table_name)
            + "->"
            + to_camel_case(field_name)
            + " = $item->"
            + field_name
            + ";"
        )

    print("        return $" + to_camel_case(table_name) + ";")
    print("    }")


def generate_model_class(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for table in root.findall("./database/table_structure"):
        table_name = table.attrib["name"]
        print("class " + to_pascal_case(table_name) + " {")

        # generate properties.
        for field in table.findall("./field"):
            field_comment = field.attrib["Comment"]
            field_name = field.attrib["Field"]
            print("    // " + field_comment)
            print("    public $" + to_camel_case(field_name) + ";")
            print("")

        # generate converter.
        generate_converter_method(table)

        print("}")


def to_pascal_case(snake_str):
    components = snake_str.split("_")
    return "".join(x.title() for x in components)


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


if __name__ == "__main__":
    args = sys.argv
    if 2 == len(args):
        filename = args[1]
        generate_model_class(filename)
    else:
        print("Usage: python gen_model.py [filename.xml]")
