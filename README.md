Language being interpreted is a subset of c++ language

<Digit>::= 0|1|2|3|4|5|6|7|8|9
<Letter>::= a-Z
<Number>::= [–]<Digit>*
<StringConstant>::="{<Letter>|<Number>}"
<Identifier>::= <letter>(<letter >|<Number>)*
<AbstractType>::=<SimpleType>|<Array>|void
<SimpleType>::= int|bool|string
<Array>::=<SimpleType>\[\]
<Operation>::=<Operation_а>|<Operation_l>|<Operation_cmp>
<Operation_а>::= +|–|*|/|%
<Operation_l>::= ! |&&| \|\|
<Operation_cmp>::=<|>|>=|<=| == | !=
<Instruction>::=[{<WhileCycle>|<If>|<Assignment>|<Print>|<Get>}]
<WhileCycle>::= While(<Condition>) <Block>
<If>::= if(<Condition>) <Block>
<Expression>::=<Expression><Operation><Expression>|<FunctionCall>|<Variable>|<Number>
<Assignment>::=<Identifier> = <Expression>
<Print>::= print <Expression>
<Get>::= get <Expression>
<Block>:= \{ [{<Instruction>}] \\}
<Condition>:=(<Expression>)
...