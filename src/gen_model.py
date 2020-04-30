import sys
import xml.etree.ElementTree as ET


def generateModelClass(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for table in root.findall("./database/table_structure"):
        tableName = table.attrib["name"]
        print("class " + to_pascal_case(tableName) + " {")

        for field in table.findall("./field"):
            fieldComment = field.attrib["Comment"]
            fieldName = field.attrib["Field"]
            print("    // " + fieldComment)
            print("    public $" + to_camel_case(fieldName) + ";")
            print("")

        print(
            "    public function to"
            + to_pascal_case(tableName)
            + "(ORM $item) : "
            + to_pascal_case(tableName)
            + " {"
        )
        print(
            "        $"
            + to_camel_case(tableName)
            + " = new "
            + to_pascal_case(tableName)
            + "();"
        )

        for field in table.findall("./field"):
            fieldName = field.attrib["Field"]
            print(
                "        $"
                + to_camel_case(tableName)
                + "->"
                + to_camel_case(fieldName)
                + " = $item->"
                + fieldName
                + ";"
            )

        print("        return $" + to_camel_case(tableName) + ";")
        print("    }")

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
        generateModelClass(filename)
    else:
        print("Usage: python gen_model.py [filename.xml]")
