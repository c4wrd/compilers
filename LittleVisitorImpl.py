from antlr4.tree.Tree import TerminalNodeImpl

from LittleParser import LittleParser
from LittleVisitor import LittleVisitor
from typing import *
from ast.nodes import *

class LittleVisitorImpl(LittleVisitor):

    def visitProgram(self, ctx: LittleParser.ProgramContext):
        return super().visitProgram(ctx)

    def visitProgram_body(self, ctx: LittleParser.Program_bodyContext):
        return super().visitProgram_body(ctx)

    def visitDecl(self, ctx: LittleParser.DeclContext):
        return super().visitDecl(ctx)

    def visitString_decl(self, ctx: LittleParser.String_declContext):
        node = LiteralNode(ctx.IDENTIFIER().getText(), LiteralTypes.STRING)
        return node

    def visitVar_decl(self, ctx: LittleParser.Var_declContext) -> List[VarDeclarationNode]:
        var_type = self.visit(ctx.var_type())
        id_nodes = self.visit(ctx.id_list())
        return [VarDeclarationNode(id_node, var_type) for id_node in id_nodes]

    def visitVar_type(self, ctx: LittleParser.Var_typeContext):
        if ctx.getText() == "INT":
            return LiteralTypes.INTEGER
        else:
            return LiteralTypes.FLOAT

    def visitAny_type(self, ctx: LittleParser.Any_typeContext):
        return super().visitAny_type(ctx)

    def visitId_list(self, ctx: LittleParser.Id_listContext) -> List[VarRefNode]:
        id_list = []
        id_list.append(VarRefNode(ctx.IDENTIFIER().getText()))
        if ctx.id_list() is not None: # add additional ids
            id_list.extend(self.visit(ctx.id_list()))
        return id_list

    def visitParam_decl_list(self, ctx: LittleParser.Param_decl_listContext):
        return super().visitParam_decl_list(ctx)

    def visitParam_decl(self, ctx: LittleParser.Param_declContext):
        return super().visitParam_decl(ctx)

    def visitParam_decl_tail(self, ctx: LittleParser.Param_decl_tailContext):
        return super().visitParam_decl_tail(ctx)

    def visitFunc_declarations(self, ctx: LittleParser.Func_declarationsContext):
        return super().visitFunc_declarations(ctx)

    def visitFunc_decl(self, ctx: LittleParser.Func_declContext):
        return super().visitFunc_decl(ctx)

    def visitFunc_body(self, ctx: LittleParser.Func_bodyContext):
        return super().visitFunc_body(ctx)

    def visitStmt_list(self, ctx: LittleParser.Stmt_listContext):
        node = StatementListNode()
        if ctx.stmt() is not None:
            node.add_child(self.visit(ctx.stmt()))
            if ctx.stmt_list() is not None:
                child_stmt_list = self.visit(ctx.stmt_list()) # StatementListNode
                for stmt in child_stmt_list.children:
                    node.add_child(stmt)
        return node

    def visitStmt(self, ctx: LittleParser.StmtContext):
        return super().visitStmt(ctx)

    def visitBase_stmt(self, ctx: LittleParser.Base_stmtContext):
        return super().visitBase_stmt(ctx)

    def visitAssign_stmt(self, ctx: LittleParser.Assign_stmtContext):
        return super().visitAssign_stmt(ctx)

    def visitAssign_expr(self, ctx: LittleParser.Assign_exprContext):
        return AssignmentNode(ctx.IDENTIFIER().getText(), self.visit(ctx.expr()))

    def visitRead_stmt(self, ctx: LittleParser.Read_stmtContext):
        node = ReadNode()
        ids = self.visit(ctx.id_list())
        for id in ids:
            node.add_child(id)
        return node

    def visitWrite_stmt(self, ctx: LittleParser.Write_stmtContext):
        node = WriteNode()
        ids = self.visit(ctx.id_list())
        for id in ids:
            node.add_child(id)
        return node

    def visitReturn_stmt(self, ctx: LittleParser.Return_stmtContext):
        return super().visitReturn_stmt(ctx)

    def visitProcessAddOp(self, ctx: LittleParser.ProcessAddOpContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(0))
        node = AddExprNode(self.visit(ctx.addop()), left, right)
        return node

    def visitProcessIdentExpr(self, ctx: LittleParser.ProcessIdentExprContext):
        return VarRefNode(ctx.IDENTIFIER().getText())

    def visitProcessFloatExpr(self, ctx: LittleParser.ProcessFloatExprContext):
        return LiteralNode(ctx.getText(), LiteralTypes.FLOAT)

    def visitProcessIntExpr(self, ctx: LittleParser.ProcessIntExprContext):
        return LiteralNode(ctx.getText(), LiteralTypes.INTEGER)

    def visitProcessMulOp(self, ctx: LittleParser.ProcessMulOpContext):
        return super().visitProcessMulOp(ctx)

    def visitProcessCallExpr(self, ctx: LittleParser.ProcessCallExprContext):
        return super().visitProcessCallExpr(ctx)

    def visitProcessParanExpr(self, ctx: LittleParser.ProcessParanExprContext):
        return self.visit(ctx.expr())

    def visitCall_expr(self, ctx: LittleParser.Call_exprContext):
        return super().visitCall_expr(ctx)

    def visitExpr_list(self, ctx: LittleParser.Expr_listContext):
        return super().visitExpr_list(ctx)

    def visitExpr_list_tail(self, ctx: LittleParser.Expr_list_tailContext):
        return super().visitExpr_list_tail(ctx)

    def visitPrimary(self, ctx: LittleParser.PrimaryContext):
        return super().visitPrimary(ctx)

    def visitAddop(self, ctx: LittleParser.AddopContext):
        return super().visitAddop(ctx)

    def visitMulop(self, ctx: LittleParser.MulopContext):
        return super().visitMulop(ctx)

    def visitIf_stmt(self, ctx: LittleParser.If_stmtContext):
        return super().visitIf_stmt(ctx)

    def visitElse_part(self, ctx: LittleParser.Else_partContext):
        return super().visitElse_part(ctx)

    def visitCond(self, ctx: LittleParser.CondContext):
        return super().visitCond(ctx)

    def visitCompop(self, ctx: LittleParser.CompopContext):
        return super().visitCompop(ctx)

    def visitWhile_stmt(self, ctx: LittleParser.While_stmtContext):
        return super().visitWhile_stmt(ctx)

    def aggregateResult(self, aggregate, nextResult):
        if aggregate == None:
            return nextResult
        elif nextResult == None:
            return aggregate
        return nextResult


