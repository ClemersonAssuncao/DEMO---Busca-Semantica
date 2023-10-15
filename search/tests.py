from django.test import TestCase
import random

# Create your tests here.
def getTestData():
    list = []
    texts = ['Roma Antiga foi uma civilização itálica que surgiu no século VIII a.C. Localizada ao longo do mar Mediterrâneo e centrada na cidade de Roma, na península Itálica, expandiu-se para se tornar um dos maiores impérios do mundo antigo, com uma estimativa de 50 a 90 milhões de habitantes e cobrindo 6,5 milhões de quilômetros quadrados no seu auge entre os séculos I e II.',
    'Em seus cerca de doze séculos de existência, a civilização romana passou de uma monarquia para a república clássica e, em seguida, para um império cada vez mais autocrático. Através da conquista e da assimilação, ele passou a dominar a Europa Ocidental e Meridional, a Ásia Menor, o Norte da África e partes da Europa Setentrional e Oriental.',
    'Roma foi preponderante em toda a região do Mediterrâneo e foi uma das mais poderosas entidades políticas do mundo antigo.',
    'É muitas vezes agrupada na Antiguidade Clássica, juntamente com a Grécia Antiga e culturas e sociedades semelhantes, que são conhecidas como o mundo greco-romano.',
    'A sociedade romana antiga contribuiu para o governo, o direito, a política, a engenharia, as artes, a literatura, a arquitetura, a tecnologia, a guerra, as religiões, as línguas e as sociedades modernas.',
    'Como uma civilização altamente desenvolvida, Roma profissionalizou e expandiu suas forças armadas e criou um sistema de governo chamado res publica, a inspiração para repúblicas modernas,[7][8][9] como os Estados Unidos e a França. Conseguiu feitos tecnológicos e arquitetônicos impressionantes, tais como a construção de um amplo sistema de aquedutos e estradas, bem como a construção de grandes monumentos, palácios e instalações públicas.',
    'Até o final da República (27 a.C.), Roma tinha conquistado as terras em torno do Mediterrâneo e além: seu domínio se estendia do oceano Atlântico à Arábia e da boca do Reno ao norte da África. O Império Romano surgiu com o início da ditadura de Augusto que encerrou o período da República. Os 721 anos de Guerras Romano-Persas começaram em 92 a.C. com a sua primeira guerra contra o Império Parta.',
    'Este se tornaria o mais longo conflito da história humana e teve grandes efeitos e consequências duradouros para ambos os impérios. Sob Trajano, o Império atingiu o seu pico territorial. Os costumes e as tradições republicanas começaram a diminuir durante o período imperial, com guerras civis tornando-se um prelúdio comum para o surgimento de um novo imperador.',
    'Estados dissidentes, como o Império de Palmira, iriam dividir temporariamente o império durante a crise do terceiro século. Atormentado pela instabilidade interna e atacado pelas invasões bárbaras, a parte ocidental do império fragmentou-se no século V, o que é visto como um marco pelos historiadores, que usam para dividir a Antiguidade Tardia da Idade das Trevas na Europa. A parte oriental do império permaneceu como uma potência durante toda a Idade Média, até a sua queda em 1453.',
    'Embora os cidadãos do império não fizessem tal distinção, o Império Oriental é mais comumente referido como "Império Bizantino" para diferenciá-lo do Estado da Antiguidade no qual ele nasceu.']
    for i in range(20):
        list.append({'id': i, 'title': 'Titulo ' + str(i), 'content': texts[random.randint(0, 9)]})
    return list

def getTestTree():
    listRandom = []
    for item in range(20):
        listRandom.append({'id': item, 'name': 'Teste Item ' + str(item) , 'link':'#' + str(item)})
    newList = []
    lastItem = None
    for item in listRandom:
        
        if (lastItem is not None):
            if ('children' not in lastItem):
                lastItem['children'] = []
            lastItem['children'].append(item)
            lastItem = None
        else:
            newList.append(item)
        if (random.randint(0, 10) < 5):
            lastItem = item
    return newList