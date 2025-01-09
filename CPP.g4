grammar CPP;

program
    : (preprocessorDirective | namespaceDirective | statement | emptyStatement)* EOF
    ;

statement
    : variableDeclaration
    | arrayDeclaration
    | arrayAssignment
    | variableChange
    | forStatement
    | whileStatement
    | doWhileStatement
    | ifStatement
    | block
    | incrementExpression
    | functionDeclaration
    | returnStatement
    | coutStatement
    | cinStatement
    | functionCall
    | emptyVariableDeclaration
    | emptyStatement
    ;

variableDeclaration
    : (INT_TYPE | STRING_TYPE) ID ASSIGN (ID | INT | STRING | arithmeticExpression | functionCall) SEMICOLON
    ;

emptyVariableDeclaration
    : (INT_TYPE | STRING_TYPE) ID SEMICOLON
    ;

variableChange
    : ID ASSIGN (ID | INT | arithmeticExpression | functionCall) SEMICOLON
    ;

forStatement
    : FOR LPAREN (variableDeclaration | variableChange) compareExpression SEMICOLON incrementExpression RPAREN block
    ;

whileStatement
    : WHILE LPAREN compareExpression RPAREN block
    ;

doWhileStatement
    : DO block WHILE LPAREN compareExpression RPAREN SEMICOLON
    ;

ifStatement
    : IF LPAREN compareExpression RPAREN block (ELSE_IF LPAREN compareExpression RPAREN block)* (ELSE block)?
    ;

functionDeclaration
    : (INT_TYPE | STRING_TYPE | VOID_TYPE) ID LPAREN parameterList? RPAREN block
    ;

arrayDeclaration
    : (INT_TYPE | STRING_TYPE) ID LBRACKET INT RBRACKET SEMICOLON
    ;

arrayAssignment
    : ID LBRACKET (INT | ID) RBRACKET ASSIGN (ID | INT | STRING | arithmeticExpression | functionCall) SEMICOLON
    ;

arrayCall
    : ID LBRACKET INT RBRACKET
    | ID LBRACKET ID RBRACKET
    ;

arrayFun
    : ID LBRACKET RBRACKET
    ;

parameterList
    : parameter (COMMA parameter)*
    ;

parameter
    : (INT_TYPE | STRING_TYPE) (ID | arrayFun)
    ;

functionCall
    : ID LPAREN argumentList? RPAREN SEMICOLON?
    ;

argumentList
    : (ID | INT | STRING | arithmeticExpression | functionCall | arrayCall) (COMMA (ID | INT | STRING | arithmeticExpression | functionCall | arrayCall))*
    ;

compareExpression
    : compareExpression (LESS | GREATER | EQUAL | NOT_EQUAL | LESS_EQUAL | GREATER_EQUAL | LOGICAL_AND | LOGICAL_OR) compareExpression
    | NOT compareExpression
    | LPAREN compareExpression RPAREN
    | ID
    | INT
    | STRING
    | arithmeticExpression
    | arrayCall
    | functionCall
    ;

arithmeticExpression
    : arithmeticExpression (PLUS | MINUS | MULTIPLY | DIVIDE | MODULO) arithmeticExpression
    | LPAREN arithmeticExpression RPAREN
    | ID
    | INT
    | functionCall
    | arrayCall
    | STRING
    ;

incrementExpression
    : ID INCREMENT SEMICOLON?
    | ID DECREMENT SEMICOLON?
    ;

returnStatement
    : RETURN (ID | INT | arithmeticExpression)? SEMICOLON
    ;

block
    : LBRACE statement* RBRACE
    ;

coutStatement
    : COUT SHIFT_LEFT (ID | INT | STRING | arithmeticExpression) (SHIFT_LEFT (ID | INT | STRING | arithmeticExpression))* SEMICOLON
    ;

cinStatement
    : CIN SHIFT_RIGHT ID (SHIFT_RIGHT ID)* SEMICOLON
    ;

preprocessorDirective
    : '#' ('include' | 'define') '<' ID '>' NEWLINE
    ;

namespaceDirective
    : 'using' 'namespace' ID SEMICOLON
    ;

emptyStatement
    : (SEMICOLON | NEWLINE)+
    ;

SEMICOLON     : ';' ;
COMMA         : ',' ;
LPAREN        : '(' ;
RPAREN        : ')' ;
LBRACKET      : '[' ;
RBRACKET      : ']' ;
LBRACE        : '{' ;
RBRACE        : '}' ;
LESS          : '<' ;
GREATER       : '>' ;
EQUAL         : '==' ;
NOT_EQUAL     : '!=' ;
LESS_EQUAL    : '<=' ;
GREATER_EQUAL : '>=' ;
LOGICAL_AND   : '&&' ;
LOGICAL_OR    : '||' ;
PLUS          : '+' ;
MINUS         : '-' ;
MULTIPLY      : '*' ;
DIVIDE        : '/' ;
MODULO        : '%' ;
SHIFT_LEFT    : '<<' ;
SHIFT_RIGHT   : '>>' ;
NOT           : '!' ;
FOR           : 'for' ;
WHILE         : 'while' ;
DO            : 'do' ;
IF            : 'if' ;
ELSE_IF       : 'else if' ;
ELSE          : 'else' ;
RETURN        : 'return' ;
ASSIGN        : '=' ;
COUT          : 'cout' ;
CIN           : 'cin' ;
INT_TYPE      : 'int' ;
STRING_TYPE   : 'string' ;
VOID_TYPE     : 'void' ;
NEWLINE       : '\n' ;

ID            : [a-zA-Z_][a-zA-Z_0-9]* ;
INT           : [0-9]+ ;
INCREMENT     : '++' ;
DECREMENT     : '--' ;
STRING        : '"' (~["\\] | '\\' .)* '"' ;
WS            : [ \t\r\n]+ -> skip ;
