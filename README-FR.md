### Concept

Le principe de l'apprentissage par renforcement est de créer un agent, libre d’entreprendre des actions dans un environnement. Ces actions modifient l’état (state) de l’agent, et ce changement d’état s’accompagne
d’une récompense (reward). Pour l’agent, le but du jeu est de maximiser ses récompenses, ce
qui le pousse à apprendre quelles actions effectuer pour obtenir le plus de récompenses.

### Mise en situation

Imaginons que nous sommes dans une rue, et je vous pose la question :

- Quel est le __meilleur restaurant__ dans lequel nous pouvons manger ?

Vous allez d'abord identifier dans quelle __rue__ nous sommes. Imaginons que nous sommes dans une __rue__ nommée __The Gourmet Avenue__. Si vous n'êtes jamais venu dans cette rue auparavant, vous ne saurez pas quoi répondre.

Comme nous n'avons pas la réponse, nous décidons d'aller dans un restaurant au hasard appelé __Burgir Restaurant__. Malheureusement, nous constatons que ce n'était pas bon du tout. Nous notons donc que lorsque nous étions dans __The Gourmet Avenue__, le __Burgir Restaurant__ n'était pas une bonne adresse.

Nous revenons le jour suivant dans cette même rue, et je vous pose la même question. Vous ne savez toujours pas quel est le meilleur restaurant, mais, en tout cas, vous savez que le __Burgir Restaurant__ est à éviter.

Nous décidons alors d'aller dans un autre restaurant appelé __Master Chicken__. Cette fois-ci, il s'avère que cette adresse est excellente. Nous notons donc que le __Master Chicken__ de __The Gourmet Avenue__ est une très bonne adresse.

À présent, la prochaine fois que je vous poserai la question, vous serez en mesure de me répondre que le meilleur restaurant que vous connaissez dans __The Gourmet Avenue__ est le __Master Chicken__.

Cela dit, rien ne nous confirme que c'est le meilleur restaurant, mais, d'après nos expériences, c'est le cas. Cependant, pour réellement connaître le meilleur restaurant, il faut explorer d'autres endroits, tester différents restaurants, et ne pas se reposer uniquement sur ce que nous connaissons déjà.

Car, imaginons que nous allons dans une autre __rue__ où nous ne sommes jamais allés, et que je vous pose la même question, la problématique du début se posera à nouveau.

C'est exactement le principe de l'apprentissage par renforcement. Pour éviter d'être dans une situation où vous serez incapable de répondre, il faut tester de nouveaux restaurants, dans d'autres rues. Au bout d'un moment, vous serez en mesure, dans n'importe quelle rue, de répondre plus ou moins à la question. Mais pour cela, il faudra tester beaucoup de restaurants...

### Résumé

Dans cette mise en situation :
- __Nous__ sommes l'__agent__.
- __Manger à une adresse__ est une __action__.
- La __rue__ et le __restaurant__ caractérisent un __état__.
- Nos __avis__ sur les __adresses__ représentent les __récompenses__.

Pour que l'agent obtienne les meilleurs résultats, il doit apprendre en visitant différents états, et, à chaque état, il obtient une récompense négative ou positive. C'est ce qui va lui permettre de créer ses expériences et de faire ses choix par la suite.

