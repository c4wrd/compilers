from LittleParser import LittleParser
from LittleVisitor import LittleVisitor

from ast.nodes import *

class LittleVisitorImpl(LittleVisitor):

    def visitExpr_list_tail(self, ctx: LittleParser.Expr_list_tailContext):
        return super().visitExpr_list_tail(ctx)

    def visitStmt_list(self, ctx: LittleParser.Stmt_listContext):
        return super().visitStmt_list(ctx)

    def visitParam_decl_list(self, ctx: LittleParser.Param_decl_listContext):
        return super().visitParam_decl_list(ctx)

    def visitFunc_decl(self, ctx: LittleParser.Func_declContext):
        return super().visitFunc_decl(ctx)

    def visitAny_type(self, ctx: LittleParser.Any_typeContext):
        return super().visitAny_type(ctx)

    def visitProcessIdentifer(self, ctx: LittleParser.ProcessIdentiferContext):
        return super().visitProcessIdentifer(ctx)

    def visitProgram_body(self, ctx: LittleParser.Program_bodyContext):
        return super().visitProgram_body(ctx)

    def visitStmt(self, ctx: LittleParser.StmtContext):
        return super().visitStmt(ctx)

    def visitWrite_stmt(self, ctx: LittleParser.Write_stmtContext):
        return super().visitWrite_stmt(ctx)

    def visitReturn_stmt(self, ctx: LittleParser.Return_stmtContext):
        return super().visitReturn_stmt(ctx)

    def visitFunc_declarations(self, ctx: LittleParser.Func_declarationsContext):
        return super().visitFunc_declarations(ctx)

    def visitVar_decl(self, ctx: LittleParser.Var_declContext):
        return super().visitVar_decl(ctx)

    def visitWhile_stmt(self, ctx: LittleParser.While_stmtContext):
        return super().visitWhile_stmt(ctx)

    def visitParam_decl_tail(self, ctx: LittleParser.Param_decl_tailContext):
        return super().visitParam_decl_tail(ctx)

    def visitId_list(self, ctx: LittleParser.Id_listContext):
        return super().visitId_list(ctx)

    def visitAssign_stmt(self, ctx: LittleParser.Assign_stmtContext):
        return super().visitAssign_stmt(ctx)

    def visitMulop(self, ctx: LittleParser.MulopContext):
        return super().visitMulop(ctx)

    def visitCompop(self, ctx: LittleParser.CompopContext):
        return super().visitCompop(ctx)

    def visitBase_stmt(self, ctx: LittleParser.Base_stmtContext):
        return super().visitBase_stmt(ctx)

    def visitFunc_body(self, ctx: LittleParser.Func_bodyContext):
        return super().visitFunc_body(ctx)

    def visitId_tail(self, ctx: LittleParser.Id_tailContext):
        return super().visitId_tail(ctx)

    def visitElse_part(self, ctx: LittleParser.Else_partContext):
        return super().visitElse_part(ctx)

    def visitDecl(self, ctx: LittleParser.DeclContext):
        return super().visitDecl(ctx)

    def visitAddop(self, ctx: LittleParser.AddopContext):
        return super().visitAddop(ctx)

    def visitExpr_list(self, ctx: LittleParser.Expr_listContext):
        return super().visitExpr_list(ctx)

    def visitPrimary(self, ctx: LittleParser.PrimaryContext):
        return super().visitPrimary(ctx)

    def visitCall_expr(self, ctx: LittleParser.Call_exprContext):
        return super().visitCall_expr(ctx)

    def visitCond(self, ctx: LittleParser.CondContext):
        return super().visitCond(ctx)

    def visitVar_type(self, ctx: LittleParser.Var_typeContext):
        return super().visitVar_type(ctx)

    def visitRead_stmt(self, ctx: LittleParser.Read_stmtContext):
        return super().visitRead_stmt(ctx)

    def visitIf_stmt(self, ctx: LittleParser.If_stmtContext):
        return super().visitIf_stmt(ctx)

    def visitProgram(self, ctx: LittleParser.ProgramContext):
        return super().visitProgram(ctx)

    def visitProcessAddOp(self, ctx: LittleParser.ProcessAddOpContext):
        return super().visitProcessAddOp(ctx)

    def visitParam_decl(self, ctx: LittleParser.Param_declContext):
        return super().visitParam_decl(ctx)

    def visitString_decl(self, ctx: LittleParser.String_declContext):
        assignment_node = AssignmentNode(ctx.IDENTIFIER(), LiteralNode(ctx.STRINGLITERAL(), LiteralTypes.STRING))

    def visitProcessIntLiteral(self, ctx: LittleParser.ProcessIntLiteralContext):
        return LiteralNode(ctx.INTLITERAL(), LiteralTypes.INTEGER)

    def visitProcessFloatLiteral(self, ctx: LittleParser.ProcessFloatLiteralContext):
        return LiteralNode(ctx.FLOATLITERAL(), LiteralTypes.FLOAT)

    def visitProcessExpr(self, ctx: LittleParser.ProcessExprContext):
        return super().visitProcessExpr(ctx)

    def visitAssign_expr(self, ctx: LittleParser.Assign_exprContext):
        return super().visitAssign_expr(ctx)

    def visitProcessCallExpr(self, ctx: LittleParser.ProcessCallExprContext):
        return super().visitProcessCallExpr(ctx)

    def visitProcessMulOp(self, ctx: LittleParser.ProcessMulOpContext):
        return super().visitProcessMulOp(ctx)

