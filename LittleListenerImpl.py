from antlr4 import *

if __name__ is not None and "." in __name__:
    from .LittleParser import LittleParser
    from .LittleListener import LittleListener
else:
    from LittleParser import LittleParser
    from LittleListener import LittleListener

class SymbolTableAttribute:
    """
    All symbol table attributes will inherit from this class
    and implement the debug method
    """

    def __init__(self, name):
        self.name = name

    def debug(self):
        raise NotImplementedError()

class StringAttribute(SymbolTableAttribute):

    def __init__(self, name, value):
        super().__init__(name)
        self.value = value

    def debug(self):
        print("name %s type STRING value %s" % (self.name, self.value))


class FloatAttribute(SymbolTableAttribute):

    def debug (self):
        print("name %s type FLOAT" % self.name)


class IntAttribute(SymbolTableAttribute):

    def debug (self):
        print("name %s type INT" % self.name)

class Scope(SymbolTableAttribute):

    def __init__(self, name, parent):
        super().__init__(name)
        self.parent = parent
        self.attributes = []
        self.records = {}
        # self.children = [] TODO determine if we need this, they can just go in attributes (?)

    def enter_scope(self, name):
        """
        1. Creates a scope with the given name
        2. Adds the scope to this scopes attributes
        3. Adds a record of the new scope
        4. Returns the new scope
        :param name: the name used to identify the scope
        :return:
        """
        scope = Scope(name, self)
        self.attributes.append(scope)
        self.records[scope.name] = scope
        return scope

    def contains_attr(self, key):
        """
        Returns whether or not a specific variable has been declared
        in the current scope (without checking parent scopes)
        """
        return key in self.records

    def resolve_attr(self, key):
        if key in self.records:
            return self.records[key]
        elif self.has_parent():
            return self.parent.resolve(key)
        else:
            return None

    def has_parent(self):
        return self.parent is not None

    def get_parent(self):
        return self.parent

    def add_attribute(self, attr: SymbolTableAttribute):
        self.attributes.append(attr)
        self.records[attr.name] = attr

    def debug(self):
        """
        Will print current scope and iterate over the children
        :return:
        """
        print("Symbol table %s" % self.name)
        for attr in self.attributes:
            attr.debug()
        print() # print an empty line

class SymbolTable:

    def __init__(self):
        self.block_id = 1
        self.global_scope = Scope("GLOBAL", None)
        self.current_scope = self.global_scope # type Scope

    def enter_scope(self, name):
        self.current_scope = self.current_scope.enter_scope(name)

    def enter_block_scope(self):
        self.current_scope = self.current_scope.enter_scope("BLOCK %d" % self.next_block_id())

    def exit_scope(self):
        if self.current_scope.has_parent():
            self.current_scope = self.current_scope.get_parent()
        else:
            raise Exception ("Cannot exit the GLOBAL scope...")

    def next_block_id(self):
        block_id = self.block_id
        self.block_id += 1
        return block_id

    def add_attribute(self, attribute: SymbolTableAttribute):
        if self.current_scope.contains_attr(attribute.name):
            raise Exception("DECLARATION ERROR %s" % attribute.name)
        else:
            self.current_scope.add_attribute(attribute)

    def debug(self, from_global=True):
        if from_global:
            while self.current_scope.has_parent():
                self.exit_scope()
        self.current_scope.debug()

class LittleListenerImpl(LittleListener):
    def __init__(self):
        self.symbol_table = SymbolTable()

    def enterAnonymousBlockScope(self):
        self.symbol_table.enter_block_scope()

    def enterNamedScope(self, name: str):
        self.symbol_table.enter_scope(name)

    def exitScope(self):
        self.symbol_table.exit_scope()

    def declareString(self, name, value):
        self.symbol_table.add_attribute(StringAttribute(name, value))

    def declareInt(self, name):
        self.symbol_table.add_attribute(IntAttribute(name))

    def declareFloat(self, name):
        self.symbol_table.add_attribute(FloatAttribute(name))

    # Enter a parse tree produced by LittleParser#program.
    def enterProgram(self, ctx: LittleParser.ProgramContext):
        pass

    # Exit a parse tree produced by LittleParser#program.
    def exitProgram(self, ctx: LittleParser.ProgramContext):
        pass

    # Enter a parse tree produced by LittleParser#program_body.
    def enterProgram_body(self, ctx: LittleParser.Program_bodyContext):
        pass

    # Exit a parse tree produced by LittleParser#program_body.
    def exitProgram_body(self, ctx: LittleParser.Program_bodyContext):
        pass

    # Enter a parse tree produced by LittleParser#decl.
    def enterDecl(self, ctx: LittleParser.DeclContext):
        pass

    # Exit a parse tree produced by LittleParser#decl.
    def exitDecl(self, ctx: LittleParser.DeclContext):
        pass

    # Enter a parse tree produced by LittleParser#string_decl.
    def enterString_decl(self, ctx: LittleParser.String_declContext):
        self.declareString(ctx.IDENTIFIER().getText(), ctx.STRINGLITERAL())

    # Exit a parse tree produced by LittleParser#string_decl.
    def exitString_decl(self, ctx: LittleParser.String_declContext):
        pass

    # Enter a parse tree produced by LittleParser#var_decl.
    def enterVar_decl(self, ctx: LittleParser.Var_declContext):
        if ctx.var_type().FLOAT() is not None:
            id_list = ctx.id_list()
            while id_list is not None and id_list.IDENTIFIER() is not None:
                self.declareFloat(id_list.IDENTIFIER().getText())
                id_list = id_list.id_tail()
        elif ctx.var_type().INT() is not None:
            id_list = ctx.id_list()
            while id_list is not None and id_list.IDENTIFIER() is not None:
                self.declareInt(id_list.IDENTIFIER().getText())
                id_list = id_list.id_tail()

    # Exit a parse tree produced by LittleParser#var_decl.
    def exitVar_decl(self, ctx: LittleParser.Var_declContext):
        pass

    # Enter a parse tree produced by LittleParser#var_type.
    def enterVar_type(self, ctx: LittleParser.Var_typeContext):
        pass

    # Exit a parse tree produced by LittleParser#var_type.
    def exitVar_type(self, ctx: LittleParser.Var_typeContext):
        pass

    # Enter a parse tree produced by LittleParser#any_type.
    def enterAny_type(self, ctx: LittleParser.Any_typeContext):
        pass

    # Exit a parse tree produced by LittleParser#any_type.
    def exitAny_type(self, ctx: LittleParser.Any_typeContext):
        pass

    # Enter a parse tree produced by LittleParser#id_list.
    def enterId_list(self, ctx: LittleParser.Id_listContext):
        pass

    # Exit a parse tree produced by LittleParser#id_list.
    def exitId_list(self, ctx: LittleParser.Id_listContext):
        pass

    # Enter a parse tree produced by LittleParser#id_tail.
    def enterId_tail(self, ctx: LittleParser.Id_tailContext):
        pass

    # Exit a parse tree produced by LittleParser#id_tail.
    def exitId_tail(self, ctx: LittleParser.Id_tailContext):
        pass

    # Enter a parse tree produced by LittleParser#param_decl_list.
    def enterParam_decl_list(self, ctx: LittleParser.Param_decl_listContext):
        pass

    # Exit a parse tree produced by LittleParser#param_decl_list.
    def exitParam_decl_list(self, ctx: LittleParser.Param_decl_listContext):
        pass

    # Enter a parse tree produced by LittleParser#param_decl.
    def enterParam_decl(self, ctx: LittleParser.Param_declContext):
        if ctx.var_type().FLOAT() is not None:
            self.declareFloat(ctx.IDENTIFIER().getText())
        else:
            self.declareInt(ctx.IDENTIFIER().getText())

    # Exit a parse tree produced by LittleParser#param_decl.
    def exitParam_decl(self, ctx: LittleParser.Param_declContext):
        pass

    # Enter a parse tree produced by LittleParser#param_decl_tail.
    def enterParam_decl_tail(self, ctx: LittleParser.Param_decl_tailContext):
        pass

    # Exit a parse tree produced by LittleParser#param_decl_tail.
    def exitParam_decl_tail(self, ctx: LittleParser.Param_decl_tailContext):
        pass

    # Enter a parse tree produced by LittleParser#func_declarations.
    def enterFunc_declarations(self, ctx: LittleParser.Func_declarationsContext):
        pass

    # Exit a parse tree produced by LittleParser#func_declarations.
    def exitFunc_declarations(self, ctx: LittleParser.Func_declarationsContext):
        pass

    # Enter a parse tree produced by LittleParser#func_decl.
    def enterFunc_decl(self, ctx: LittleParser.Func_declContext):
        self.enterNamedScope(ctx.IDENTIFIER().getText())

    # Exit a parse tree produced by LittleParser#func_decl.
    def exitFunc_decl(self, ctx: LittleParser.Func_declContext):
        self.exitScope()

    # Enter a parse tree produced by LittleParser#func_body.
    def enterFunc_body(self, ctx: LittleParser.Func_bodyContext):
        pass

    # Exit a parse tree produced by LittleParser#func_body.
    def exitFunc_body(self, ctx: LittleParser.Func_bodyContext):
        pass

    # Enter a parse tree produced by LittleParser#stmt_list.
    def enterStmt_list(self, ctx: LittleParser.Stmt_listContext):
        pass

    # Exit a parse tree produced by LittleParser#stmt_list.
    def exitStmt_list(self, ctx: LittleParser.Stmt_listContext):
        pass

    # Enter a parse tree produced by LittleParser#stmt.
    def enterStmt(self, ctx: LittleParser.StmtContext):
        pass

    # Exit a parse tree produced by LittleParser#stmt.
    def exitStmt(self, ctx: LittleParser.StmtContext):
        pass

    # Enter a parse tree produced by LittleParser#base_stmt.
    def enterBase_stmt(self, ctx: LittleParser.Base_stmtContext):
        pass

    # Exit a parse tree produced by LittleParser#base_stmt.
    def exitBase_stmt(self, ctx: LittleParser.Base_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#assign_stmt.
    def enterAssign_stmt(self, ctx: LittleParser.Assign_stmtContext):
        pass

    # Exit a parse tree produced by LittleParser#assign_stmt.
    def exitAssign_stmt(self, ctx: LittleParser.Assign_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#assign_expr.
    def enterAssign_expr(self, ctx: LittleParser.Assign_exprContext):
        pass

    # Exit a parse tree produced by LittleParser#assign_expr.
    def exitAssign_expr(self, ctx: LittleParser.Assign_exprContext):
        pass

    # Enter a parse tree produced by LittleParser#read_stmt.
    def enterRead_stmt(self, ctx: LittleParser.Read_stmtContext):
        pass

    # Exit a parse tree produced by LittleParser#read_stmt.
    def exitRead_stmt(self, ctx: LittleParser.Read_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#write_stmt.
    def enterWrite_stmt(self, ctx: LittleParser.Write_stmtContext):
        pass

    # Exit a parse tree produced by LittleParser#write_stmt.
    def exitWrite_stmt(self, ctx: LittleParser.Write_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#return_stmt.
    def enterReturn_stmt(self, ctx: LittleParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by LittleParser#return_stmt.
    def exitReturn_stmt(self, ctx: LittleParser.Return_stmtContext):
        pass

    # Enter a parse tree produced by LittleParser#expr.
    def enterExpr(self, ctx: LittleParser.ExprContext):
        pass

    # Exit a parse tree produced by LittleParser#expr.
    def exitExpr(self, ctx: LittleParser.ExprContext):
        pass

    # Enter a parse tree produced by LittleParser#call_expr.
    def enterCall_expr(self, ctx: LittleParser.Call_exprContext):
        pass

    # Exit a parse tree produced by LittleParser#call_expr.
    def exitCall_expr(self, ctx: LittleParser.Call_exprContext):
        pass

    # Enter a parse tree produced by LittleParser#expr_list.
    def enterExpr_list(self, ctx: LittleParser.Expr_listContext):
        pass

    # Exit a parse tree produced by LittleParser#expr_list.
    def exitExpr_list(self, ctx: LittleParser.Expr_listContext):
        pass

    # Enter a parse tree produced by LittleParser#expr_list_tail.
    def enterExpr_list_tail(self, ctx: LittleParser.Expr_list_tailContext):
        pass

    # Exit a parse tree produced by LittleParser#expr_list_tail.
    def exitExpr_list_tail(self, ctx: LittleParser.Expr_list_tailContext):
        pass

    # Enter a parse tree produced by LittleParser#primary.
    def enterPrimary(self, ctx: LittleParser.PrimaryContext):
        pass

    # Exit a parse tree produced by LittleParser#primary.
    def exitPrimary(self, ctx: LittleParser.PrimaryContext):
        pass

    # Enter a parse tree produced by LittleParser#addop.
    def enterAddop(self, ctx: LittleParser.AddopContext):
        pass

    # Exit a parse tree produced by LittleParser#addop.
    def exitAddop(self, ctx: LittleParser.AddopContext):
        pass

    # Enter a parse tree produced by LittleParser#mulop.
    def enterMulop(self, ctx: LittleParser.MulopContext):
        pass

    # Exit a parse tree produced by LittleParser#mulop.
    def exitMulop(self, ctx: LittleParser.MulopContext):
        pass

    # Enter a parse tree produced by LittleParser#if_stmt.
    def enterIf_stmt(self, ctx: LittleParser.If_stmtContext):
        self.enterAnonymousBlockScope()

    # Exit a parse tree produced by LittleParser#if_stmt.
    def exitIf_stmt(self, ctx: LittleParser.If_stmtContext):
        self.exitScope()

    # Enter a parse tree produced by LittleParser#else_part.
    def enterElse_part(self, ctx: LittleParser.Else_partContext):
        if ctx.children is not None:
            self.enterAnonymousBlockScope()

    # Exit a parse tree produced by LittleParser#else_part.
    def exitElse_part(self, ctx: LittleParser.Else_partContext):
        if ctx.children is not None:
            self.exitScope()

    # Enter a parse tree produced by LittleParser#cond.
    def enterCond(self, ctx: LittleParser.CondContext):
        pass

    # Exit a parse tree produced by LittleParser#cond.
    def exitCond(self, ctx: LittleParser.CondContext):
        pass

    # Enter a parse tree produced by LittleParser#compop.
    def enterCompop(self, ctx: LittleParser.CompopContext):
        pass

    # Exit a parse tree produced by LittleParser#compop.
    def exitCompop(self, ctx: LittleParser.CompopContext):
        pass

    # Enter a parse tree produced by LittleParser#while_stmt.
    def enterWhile_stmt(self, ctx: LittleParser.While_stmtContext):
        self.enterAnonymousBlockScope()

    # Exit a parse tree produced by LittleParser#while_stmt.
    def exitWhile_stmt(self, ctx: LittleParser.While_stmtContext):
        self.exitScope()