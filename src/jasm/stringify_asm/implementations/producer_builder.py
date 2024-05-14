from jasm.global_definitions import (
    DisassStyle,
    InputFileType,
)
from jasm.stringify_asm.abstracts.asm_parser import AsmParser
from jasm.stringify_asm.abstracts.disassembler import Disassembler
from jasm.stringify_asm.implementations.composable_producer import ComposableProducer, IInstructionProducer
from jasm.stringify_asm.implementations.gnu_objdump.gnu_objdump_disassembler import GNUObjdumpDisassembler
from jasm.stringify_asm.implementations.gnu_objdump.gnu_objdump_parser_manual import ObjdumpParserManual
from jasm.stringify_asm.implementations.null_disassembler import NullDisassembler


class ProducerBuilder:
    """Builder for the producer."""

    @staticmethod
    def build(file_type: InputFileType, assembly_style: DisassStyle = DisassStyle.att) -> IInstructionProducer:
        """Create a producer based on the file type."""

        # Logic for choosing diferent type of parser should be here

        parser: AsmParser = ObjdumpParserManual()
        disassembler: Disassembler

        # Logic for choosing diferent type of disassembler should be here
        match file_type:
            case InputFileType.binary:
                disassembler = GNUObjdumpDisassembler(enum_disas_style=assembly_style)
            case InputFileType.assembly:
                disassembler = NullDisassembler()
            case _:
                raise ValueError("Either assembly or binary must be provided")

        return ComposableProducer(disassembler=disassembler, parser=parser)
