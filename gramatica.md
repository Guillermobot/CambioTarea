Gramatica 


Programa y Sentencias
Program      → StmtList
StmtList     → Stmt StmtList | ε
Stmt         → Decl ';'
             | Assign ';'
             | IfStmt
             | WhileStmt
             | PrintStmt ';'
             | Block
Decl         → Type id DeclInit
DeclInit     → '=' Expr | ε
Type         → int | float | string
Assign       → id '=' Expr
IfStmt       → If '(' Expr ')' Stmt ElseOpt
ElseOpt      → Else Stmt | ε
WhileStmt    → While '(' Expr ')' Stmt
PrintStmt    → print '(' ArgListOpt ')'
ArgListOpt   → ArgList | ε
ArgList      → Expr ArgList'
ArgList'     → ',' Expr ArgList' | ε
Block        → '{' StmtList '}'
Expr         → OrExpr
OrExpr       → AndExpr OrTail
OrTail       → '||' AndExpr OrTail | ε
AndExpr      → RelExpr AndTail
AndTail      → '&&' RelExpr AndTail | ε
RelExpr      → AddExpr RelTail
RelTail      → RelOp AddExpr | ε
RelOp        → '==' | '!=' | '<' | '<=' | '>' | '>='
AddExpr      → MulExpr AddTail
AddTail      → ('+' | '-') MulExpr AddTail | ε
MulExpr      → Unary MulTail
MulTail      → ('*' | '/' | '%') Unary MulTail | ε
Unary        → '!' Unary | '-' Unary | Primary
Primary      → id | NUM | '(' Expr ')'



Ejemplo de código válido según la gramática
int x;
float total;
x = 5 + 3;
if (x < 10) {
    print(x);
} else {
    x = x + 1;
}
























FIRST 

Programa y sentencias
FIRST(Type) = { int, float, string }


FIRST(DeclInit) = { '=', ε }


FIRST(Decl) = { Int, float, string }


FIRST(Assign) = { id }


FIRST(IfStmt) = { If }


FIRST(ElseOpt) = { Else, ε }


FIRST(WhileStmt) = { While}
FIRST(PrintStmt) = { Print }


FIRST(Block) = { '{' }


FIRST(Stmt) = { int, float, string, id, if, while, print, '{' }


FIRST(StmtList) = { int, float, string,  id, if, while, print, '{', ε }


FIRST(Program) = {int, float, id, string, ff, while, print, '{', ε }



FIRST(ArgList') = { ',', ε }


FIRST(ArgList) = { '!', '-', id, num, '(' } ← (hereda de Expr)


FIRST(ArgListOpt) = { '!', '-', id, num, '(', ε }





FIRST(Primary) = { id, num, '(' }


FIRST(Unary) = { '!', '-', id, num, '(' }


FIRST(MulTail) = { '*', '/', '%', ε }


FIRST(MulExpr) = { '!', '-', id, num, '(' }


FIRST(AddTail) = { '+', '-', ε }


FIRST(AddExpr) = { '!', '-', id, num, '(' }


FIRST(RelOp) = { '==', '!=', '<', '<=', '>', '>=' }


FIRST(RelTail) = { '==', '!=', '<', '<=', '>', '>=', ε }


FIRST(RelExpr) = { '!', '-', id, num, '(' }


FIRST(AndTail) = { '&&', ε }


FIRST(AndExpr) = { '!', '-', id, num, '(' }


FIRST(OrTail) = { '||', ε }


FIRST(OrExpr) = { '!', '-', id, NUM, '(' }


FIRST(Expr) = { '!', '-', id, num, '(' }










FOLLOW

FOLLOW(PROGRAM) = { $ }


FOLLOW(STMT_LIST) = { '}', $ }


FOLLOW(STMT) = { int, float, string,  id, if, while, print, '{', else, '}', $ }


FOLLOW(BLOCK) = FOLLOW(STMT) = { int, float, id, if, while, print, '{', else, '}', $ }

FOLLOW(TYPE) = { id }


FOLLOW(DECL_INIT) = { ';' }


FOLLOW(DECL) = { ';' }


FOLLOW(ASSIGN) = { ';' }


FOLLOW(IF_STMT) = FOLLOW(STMT) = { int, float, string,  id, if, while, print, '{', else, '}', $ }


FOLLOW(ELSE_OPT) = FOLLOW(IF_STMT) = { int, float,string,  id, if, while, print, '{', '}', $ }


FOLLOW(WHILE_STMT) = FOLLOW(STMT) = { int, float, string, id, if, while, print, '{', else, '}', $ }


FOLLOW(PRINT_STMT) = { ';' }


FOLLOW(ARG_LIST_TAIL) = { ')' }


FOLLOW(ARG_LIST) = { ')' }


FOLLOW(ARG_LIST_OPT) = { ')' }



FOLLOW(EXPR) = { ')', ',', ';' }


FOLLOW(OR_EXPR) = FOLLOW(EXPR) = { ')', ',', ';' }


FOLLOW(OR_TAIL) = FOLLOW(OR_EXPR) = { ')', ',', ';' }


FOLLOW(AND_EXPR) = { '||', ')', ',', ';' }


FOLLOW(AND_TAIL) = { '||', ')', ',', ';' }


FOLLOW(REL_EXPR) = { '&&', '||', ')', ',', ';' }


FOLLOW(REL_TAIL) = FOLLOW(REL_EXPR) = { '&&', '||', ')', ',', ';' }


FOLLOW(ADD_EXPR) = { '==','!=','<','<=','>','>=', '&&', '||', ')', ',', ';' }


FOLLOW(ADD_TAIL) = FOLLOW(ADD_EXPR) = { '==','!=','<','<=','>','>=', '&&', '||', ')', ',', ';' }


FOLLOW(MUL_EXPR) = { '+','-', '==','!=','<','<=','>','>=', '&&', '||', ')', ',', ';' }


FOLLOW(MUL_TAIL) = FOLLOW(MUL_EXPR) = { '+','-', '==','!=','<','<=','>','>=', '&&', '||', ')', ',', ';' }


FOLLOW(UNARY) = { '*','/','%', '+','-', '==','!=','<','<=','>','>=', '&&','||', ')', ',', ';' }


FOLLOW(PRIMARY) = FOLLOW(UNARY) = { '*','/','%', '+','-', '==','!=','<','<=','>','>=', '&&','||', ')', ',', ';' }


FOLLOW(REL_OP) = { '!', '-', id, num, '(' }
 proviene de REL_TAIL → REL_OP ADD_EXPR)






