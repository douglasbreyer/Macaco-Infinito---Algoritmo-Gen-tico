#===============================================================================
# Pyevolve version of the Infinite Monkey Theorem
# See: http://en.wikipedia.org/wiki/Infinite_monkey_theorem
#===============================================================================

from pyevolve import G1DList
from pyevolve import GSimpleGA, Consts
from pyevolve import Selectors
from pyevolve import Initializators, Mutators, Crossovers
import math

sentence = raw_input("Entre com a frase a ser encontrada pelos macacos: ")
numeric_sentence = map(ord, sentence)    #aplica o ord(converte o caractere para o numero correspondente na tabela ASCI) em cada caractere da lista/string

def evolve_callback(ga_engine):                           #funcao local ga_engine eh uma instancia do modulo GSimpleGA / mecanismo do algoritmo genetico  http://pyevolve.sourceforge.net/getstarted.html?highlight=ga_engine
   generation = ga_engine.getCurrentGeneration()              #obter a geracao atual 
   if generation%50==0:        #intervalo mostrar os dados
      indiv = ga_engine.bestIndividual()          #retorna a melhor individuo
      print ''.join(map(chr,indiv))                 #devolce o caractere correspondente ao codigo numerico passado
   return False

def run_main():
   genome = G1DList.G1DList(len(sentence))          #instanciando uma classe do tipo G1DList (representacao do cromossomo 1D List)
   genome.setParams(rangemin=min(numeric_sentence),         #definindo parametros iniciais. 
                    rangemax=max(numeric_sentence),
                    bestrawscore=0.00,
                    gauss_mu=1, gauss_sigma=4)           #menor codigo numerico, mairo codigo numerico, best score, media, desvio padrao http://pyevolve.sourceforge.net/module_mutators.html?highlight=g1dlistmutatorintegergaussian#Mutators.G1DListMutatorIntegerGaussian

   genome.initializator.set(Initializators.G1DListInitializatorInteger)      #iniciliza funcao de inteiros de G1Dlist
   genome.mutator.set(Mutators.G1DListMutatorIntegerGaussian)               #aplica a mutacao gaussiana onde a media eh 0 e o desvio padrao eh 
   genome.evaluator.set(lambda genome: sum(                             #chamada para avaliar o genoma
                           [abs(a-b) for a, b in zip(genome, numeric_sentence)]      #FITNESS
                        ))

   ga = GSimpleGA.GSimpleGA(genome)                               #manda o genoma pro algoritmo genetico 
   # ga.stepCallback.set(evolve_callback)
   ga.setMinimax(Consts.minimaxType["minimize"])              #seta para minimizar
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)     # criterio de parada usando o best score bruto
   ga.setPopulationSize(60)             #tamanho da populacao
   ga.setMutationRate(0.02)           #taxa de mutacao entre 0 e 1
   ga.setCrossoverRate(0.9)           #taxa de cruzamento entre 0 e 1
   ga.setGenerations(5000)            #numero maximo de geracoes de evolucao
   ga.evolve(freq_stats=100)          #faz geracoes ate o criterio de termino e exibe as informacoes. 

   best = ga.bestIndividual()           #retorna o melhor individuo da populacao
   print "Best individual score: %.2f" % (best.score,)    #printa score do melhor
   print ''.join(map(chr, best))       #retorna os caracteres correspondentes ao codigo numerico passado

if __name__ == "__main__":             
   run_main()