predicate pre_original(x:int,r:int){
  x==1
}

predicate pre_gen(x:int,r:int)
{
  true // (#PRE) && ... (#PRE)
}

lemma pre_eq(x:int,r:int)
  ensures pre_original(x,r ) <==> pre_gen(x,r )
{
}

predicate post_original(x:int,r:int)
  requires pre_original(x,r){
  ( r==3*x)
}

predicate post_gen(x:int,r:int)
  requires pre_original(x,r){
  true // (#POST) && ... (#POST)
}

lemma post_eq(x:int,r:int)
  requires pre_original(x,r )
  requires pre_gen(x,r )
  ensures post_original(x,r ) <==> post_gen(x,r )
{
}
