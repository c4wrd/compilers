grammar Little;

/** PARSE RULES **/
program : PROGRAM IDENTIFIER BEGIN program_body END ;
program_body : decl func_declarations ;
decl : ( string_decl decl | var_decl decl )? ;

// Global String Declaration
string_decl : STRING IDENTIFIER ':=' STRINGLITERAL ';' ;

// Variable Declarations
var_decl : var_type id_list ';' ;
var_type : FLOAT | INT ;
any_type : var_type | VOID ;
id_list : IDENTIFIER id_tail ;
id_tail : (',' IDENTIFIER id_tail )? ;

// Function Parameter List
param_decl_list : (param_decl param_decl_tail)? ;
param_decl : var_type IDENTIFIER;
param_decl_tail : (',' param_decl param_decl_tail)? ;

// Function Declarations
func_declarations : (func_decl func_declarations)? ;
func_decl : FUNCTION any_type IDENTIFIER '(' param_decl_list ')' BEGIN func_body END ;
func_body : decl stmt_list ;

// Statement List
stmt_list : (stmt stmt_list)? ;
stmt : base_stmt | if_stmt | while_stmt ;
base_stmt : assign_stmt | read_stmt | write_stmt | return_stmt ;

// Basic Statements
assign_stmt : assign_expr ';' ;
assign_expr : IDENTIFIER ':=' expr ;
read_stmt : READ '(' id_list ')' ';' ;
write_stmt : WRITE '(' id_list ')' ';' ;
return_stmt : RETURN expr ';' ;

// Expressions

expr
    : expr addop expr #processAddOp
    | expr mulop expr   #processMulOp
    | IDENTIFIER    #processIdentifer
    | INTLITERAL    #processIntLiteral
    | FLOATLITERAL  #processFloatLiteral
    | '(' expr ')'  #processExpr
    | call_expr #processCallExpr
;


/*expr : expr_prefix factor ;
expr_prefix : expr_prefix factor addop
    | // empty
    ;
factor : factor_prefix postfix_expr ;
factor_prefix
    : factor_prefix postfix_expr mulop
    | // empty
    ;
postfix_expr : primary | call_expr ; */
call_expr : IDENTIFIER '(' expr_list ')' ;
expr_list : (expr expr_list_tail)? ;
expr_list_tail : (',' expr expr_list_tail)? ;
primary
    : '(' expr ')'
    | IDENTIFIER
    | INTLITERAL
    | FLOATLITERAL
;
addop : '+' | '-' ;
mulop : '*' | '/' ;

// Complex statements and conditions
if_stmt : IF '(' cond ')' decl stmt_list else_part ENDIF ;
else_part : (ELSE decl stmt_list)? ;
cond : expr compop expr ;
compop
    : '<'
    | '>'
    | '='
    | '!='
    | '<='
    | '>='
    ;

// while statements
while_stmt : WHILE '(' cond ')' decl stmt_list ENDWHILE ;

/** TOKENS **/

PROGRAM : 'PROGRAM' ;
BEGIN : 'BEGIN' ;
END : 'END' ;
FUNCTION : 'FUNCTION' ;
READ : 'READ' ;
WRITE : 'WRITE' ;
IF : 'IF' ;
ELSE : 'ELSE' ;
FI : 'FI' ;
FOR : 'FOR' ;
ROF : 'ROF' ;
RETURN : 'RETURN' ;
INT : 'INT' ;
VOID : 'VOID' ;
STRING : 'STRING' ;
FLOAT : 'FLOAT' ;
WHILE : 'WHILE' ;
ENDIF : 'ENDIF' ;
ENDWHILE : 'ENDWHILE' ;

OPERATOR : ':=' | '+' | '-' | '*' | '/' | '=' | '!=' | '<' | '>' | '(' | ')' | ';' | ',' | '<=' | '>=' ;

IDENTIFIER : [a-zA-Z] [a-zA-Z0-9]* ;

STRINGLITERAL : '"' ~["]* '"' ;

INTLITERAL : DIGIT+ ;

FLOATLITERAL : DIGIT+ '.' DIGIT+
    | '.' DIGIT+ ;

fragment DIGIT : [0-9] ;

WHITESPACE : [ \t\r\n]+ -> skip ;

COMMENT : '--' ~[\r\n]* -> skip ;