import yaml
import argparse
from typing import Any, List, Dict, TypeAlias

Command: TypeAlias = List[Any] | Dict[str, Any] | str


class YamlHandler:
    def __init__(self) -> None:
        pass

    def read_yaml(self, file) -> Any:
        with open(file, 'r', encoding='utf-8') as f:
            loaded_yaml = yaml.load(stream=f.read(), Loader=yaml.Loader)
        return loaded_yaml

    def process_any(self, not_any: Command) -> str:
        return 'any'

    def process_not(self, not_com: Command) -> str:
        return 'not'

    def process_mov(self, mov_com: Command) -> str:
        return 'mov'

    def process_dict(self, com) -> str:
        match list(com.keys())[0]:
            case '$any':
                return self.process_any(com)
            case '$not':
                return self.process_not(com)
            case 'mov':
                return self.process_mov(com)
            case _:
                raise ValueError('Invalid YAML input.')

    def handle_yaml_command(self, com: Command) -> str:
        print(f'La entrada es: {com}')

        if isinstance(com, dict):
            return self.process_dict(com)
        elif isinstance(com, str):
            return com
        else:
            # TODO implementar excepcion para tipos no soportados por el programa
            raise ValueError("Command type not valid")

    def produce_regex_from_yaml(self, loaded_yaml: Any):
        output_regex = ''
        for command in loaded_yaml['commands']:
            output_regex += self.handle_yaml_command(command)
        return output_regex

    def main(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input-yaml', required=True)
        args = parser.parse_args()

        loaded_yaml = self.read_yaml(args.input_yaml)

        print(loaded_yaml)

        output_regex = self.produce_regex_from_yaml(loaded_yaml)

        print(f"The output regex is: {output_regex}")


if __name__ == "__main__":
    YamlHandler().main()
