D'apres la formule de l'énoncé,  nous avons deux caluls de probabilités, avec logarithm et sans logarithm 

  *spam_probability in body
          *if logarithm_way 
                   p_spam += voc_data["p_body_spam"][word].log10()
          *else 
                   p_spam *= voc_data["p_body_spam"][word] 
 *spam_probability outside body
          *if logarithm_way 
                   p_spam += 1.0/(len(voc_data["p_body_spam"][word])+1.0).log10()
          *else 
                    p_spam *= 1.0/(len(voc_data["p_body_spam"][word].)+1.0)

On fait la meme chose pour le ham en remplacant par p_ham et p_body_ham

au final on aura 
*if logarithm_way 
           puisque nous voulons la reponse en decimale et non en logarithme, nous devons transformer p_spam en decimal 
            p_spam *= 0.5925.log10();
            p_spam = pow(p_spam,10);
            
*else
            p_spam *=0.5925
meme chose pour p_ham mais on utilise 0.4075




Ces modifications seront dans la fonction spam_ham_body_prob et spam_ham_subject_probaility du fichier email analyser
 
cette fonction aura donc la variable is_logarithm_way en plus  dans la liste de ses parametre


Pour le calucul des probaiblités combinés, le systeme doit savoir si celle-ci doit se faire par logarithme our pas également, donc il nous faudra la variable is_logarithm_way_for_merged_probabilities en plus  dans la liste de ses parametre



  if is_logarithm_way_for_merged_probabilities:
     on retransforme en logarithme et on utilise la formule du calcul combiantoire
     p_spam = p_subject_spam).log10() *0.6 + p_body_spam.log10*(0.4)
      on retransforme en décimal 
     p_spam = pow(p_spam, 10) 
   else 
      p_spam = 0.6 * p_subject_spam + 0.4 * p_body_spam
   
  on fait pareil pour p_ham 
       
DISCUSSION: Je ne comprends pas pk on utilise de parametres differents de log alors que nous pouvons faire un seul. si l utilisateur utilise log pour le calcul simple, alors c est sur que le calcul combinatoire utilisera log right? 



///// creation du vocabulaire

    Il va nous falloir un deuxieme groupe de tableau dans lesquels si l occurence dans chaque tableau du premier groupe est supérieure ou égale  a la fréquence desiree, on la met dans le tableau du 2nd groupe, sinon on ne fait rien. cette implémentation sera faite dans le fichier vocabulary_creator.py

///// nettoyage 

on a just a ajouter un boolean "stemming"  dans la methode clean_text dans text_cleaner.py et remplacer 
text = self.stem_words(text)
par 
if stemming text = self.stem_words(text)


le résumé des modifications apportés sur les définitions des méthodes : 

dans text_cleaner.py : clean_text(`self`,text)  devient: clean_text(`self`,text,stemming)

dans vocabulary_creator.py : create_vocab(`self`) devient create_voca(`self`,desired_frequecy,stemming)

                             clean_text aussi se voit le parametre stemming ajouté

dans email_analyser.py is_spam(self, subject_orig, body_orig,) devient  is_spam(self, subject_orig, body_orig,logarithm_way_probs,logarithm_way_merged_probs,stemming) car utilise clean_text de text_cleaner aussi 

Les modifications apportés dans le renege.py seront donc 

 process_email(self) devient  
process_email(self,logarithm_way_probs,logarithm_way_merged_probs,stemming) car va utiliser is_spam de email_analyser pour intilialers sa variable is_spam

 classify_email(self) devient 
classify_emails(self,logarithm_way_probs,logarithm_way_merged_probs,stemming) car va utiliser process_email
