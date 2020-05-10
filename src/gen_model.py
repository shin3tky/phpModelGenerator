import sys
import xml.etree.ElementTree as ET


def generate_converter_method(table):
    buff = []
    table_name = table.attrib["name"]
    buff.append(
        "    public function to"
        + to_pascal_case(table_name)
        + "(ORM $item) : "
        + to_pascal_case(table_name)
        + " {"
    )
    buff.append(
        "        $"
        + to_camel_case(table_name)
        + " = new "
        + to_pascal_case(table_name)
        + "();"
    )

    for field in table.findall("./field"):
        field_name = field.attrib["Field"]
        buff.append(
            "        $"
            + to_camel_case(table_name)
            + "->"
            + to_camel_case(field_name)
            + " = $item->"
            + field_name
            + ";"
        )

    buff.append("        return $" + to_camel_case(table_name) + ";")
    buff.append("    }")
    return buff


def generate_tostring_method(table):
    buff = []
    buff.append("    public function __toString() {")
    buff.append("        $result = [];")

    for field in table.findall("./field"):
        field_name = field.attrib["Field"]
        buff.append(
            "        $result[] = '"
            + to_camel_case(field_name)
            + ":[' . $this->"
            + to_camel_case(field_name)
            + " . ']"
            + "';"
        )

    buff.append("        return implode(',', $result);")
    buff.append("    }")
    return buff


def generate_model_class(filename):
    buff = []
    tree = ET.parse(filename)
    root = tree.getroot()
    for table in root.findall("./database/table_structure"):
        table_name = table.attrib["name"]
        buff.append("class " + to_pascal_case(table_name) + " {")

        # generate properties.
        for field in table.findall("./field"):
            field_comment = field.attrib["Comment"]
            field_name = field.attrib["Field"]
            buff.append("    // " + field_comment)
            buff.append("    public $" + to_camel_case(field_name) + ";")
            buff.append("")

        # generate converter.
        method = generate_converter_method(table)
        buff.append("\n".join(method))

        buff.append("")

        tostring = generate_tostring_method(table)
        buff.append("\n".join(tostring))

        buff.append("}")
    return buff


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
        buff = generate_model_class(filename)
        print("\n".join(buff))
    else:
        print("Usage: python gen_model.py [filename.xml]")
