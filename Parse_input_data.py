
# coding: utf-8

# # Описание кода
# 
# В коде задается 3 класса: организм, АТФаза и последовательность. Они все имеют постфикс "pre", птому что далее классы со схожими названиями используются при задании базы данных.
# Все классы устроены схожим образом, в функции __init__ перечислены поля, которые потом будут переноситься в базу, а также списки дочерних объектов. У организма это ферменты, у ферментов - последовательности.Общей является функция __check__: она проверяет, были ли заполнены поля. У последовательности это функция __pre_check__, она сканирует строку и говорит, соотвествует ли она формату, нет ли там пустых полей(кроме поля с комментариями). То есть у класса последовательность надо запускать функцию __pre_check__ до записи данных в объект(о записи будет чуть позже), а объекты организм и фермент - после.
# 
# Есть и защита для строк в целом. Если в начале не стоит идентификатора, то строка пишется в переменную __broken_string__ и выводится после завершения работы.
# 
# ### Запись данных в объекты класса
# Класс организм и последовательность получают на вход строку из файла с информацией, а классу Atpase_pre ничего на вход не нужно. Это потому что для первых двух я предпочла написать функцию парсинга строки прямо внутри класса, она называется __parce__, а для АТФаз это не понадобилось.

# In[2]:


class Organism_pre(object):
    def __init__(self, list_1):
        self.field_type = list_1[0] 
        self.field_info = list_1[1] #second part of the line, where name and id are stated
        self.name = ''
        self.id = ''
        self.taxonomy = ''
        self.fof1 = [] # Atpase_pre objects are added here
        
        
    def check(self):
        warnings = []
        happy_messages = []
        if self.name == '':
            warnings.append('Warning! Name is not stated')
        if self.id == '':
            warnings.append('Warning! Id is not stated')
        if self.taxonomy == '':
            warnings.append('Warning! Taxonomy is not stated')
        if warnings == []:
            happy_messages.append('We checked {}, everything is fine'.format(self.name))
            happy_messages.reverse()
            #print('. '.join(happy_messages))
        else:
            print('\n'.join(warnings))
        return 0
        
    def parce(self):
        parce_l = self.field_info.strip().split()
        self.name = parce_l.pop(0) + ' ' + parce_l.pop(0)
        self.id = ' '.join(parce_l)
        return 0


# In[3]:


class Atpase_pre(object):
    def __init__(self):
        self.type = ''
        self.operon_num = 0
        self.subunit_names = []
        self.subunits = [] #Subunit_pre objects are added here
        self.additional_proteins = [] #
        self.field_list = ['Organism', 'Taxonomy', 'Type', 'Operon number', 'Additional_protein']
        self.subunit_list = [['alpha'], ['beta'], ['gamma'], ['delta'], ['epsilon'], ['A'], ['B', 'B1', 'B2'], ['C'], ['I2']]
        
    def check(self):
        warnings = []
        happy_messages = []
        if self.type == '':
            warnings.append('Warning! FoF1 type is not stated')
        if self.operon_num == 0:
            warnings.append('Warning! Operon number is not stated')
        if self.subunits == []:
            warnings.append('Warning! No subunits found')
        else:
            lost_subunits = [] # We need to check, whether all important subunits are presented. 
            #Subunit B can be presented as B or as B1 and B2, so we try to take it into concideration.
            #That is why self.subunit_list is a list of lists. Subunit can be presented in different ways.
            for i in self.subunit_list:
                count = []
                for j in i:
                    if j not in self.subunit_names:
                        count.append('No')
                    else:
                        count.append('Yes')
                if 'Yes' not in count:
                    lost_subunits.append(i[0])
                    happy_messages.append('Subunit {} is not presented.'.format(i[0]))
            if lost_subunits != []: #Some crappy and useless additions.
                lol = 0
                #happy_messages.append('These subunits are absent: {}'.format(', '.join(lost_subunits)))
            else:
                happy_messages.append('All subunits were found')
        if self.subunit_names == []:
            warnings.append('Warning! Subunit names are not stated')
        if warnings == []:
            happy_messages.append('We checked {}, everything is fine. Additional proteins: {}'.format(self.type, len(self.additional_proteins)))
            happy_messages.reverse()
            #print('. '.join(happy_messages))
        else:
            print('\n'.join(warnings))
        return 0


# In[4]:


class Subunit_pre(object):
    def __init__(self, list_1):
        self.field_type = list_1[0]
        self.field_info = list_1[1]
        self.id = ''
        self.operon = 0
        self.start = 0
        self.end = 0
        self.seq = ''
        self.comment = ''
        self.field_list = ['ProtID', 'Operon', 'Start', 'End', 'Sequence', 'Comments']
        self.field_check = ['No', 'No', 'No', 'No', 'No', 'No']
    
    
    def pre_check(self):
        ok = True
        parce_l = self.field_info.strip().split(';')
        if parce_l[-1] == '':
            parce_l.pop(-1)
        for i in parce_l:
            if '-' not in i: #looking for right dividers
                print("Warning! {} has no divider. This element won't be recognised.".format(i))
                ok = False
            else:
                field = i.strip().split('-')
                if (field[0] == '') or (field[0] != 'Comments ' and field[1]) == '': #check for emptiness
                    print('Warning! Some fields in {} are empty'.format(i))
                for f in range(len(self.field_list)):
                    if field[0].strip() in self.field_list[f]:
                        self.field_check[f] = 'Yes'
        lost_fields = []
        while 'No' in self.field_check:
            ok = False
            ind = self.field_check.index('No')
            self.field_check.pop(ind)
            a = self.field_list.pop(ind)
            lost_fields.append(a)
        if lost_fields != []:
            print("Warning! Some fields were not found: " + ", ".join(lost_fields))
        #print('Subunit {} check is complete'.format(self.field_type))
        return(ok)
    
    def parce(self):
        parce_l = self.field_info.strip().split(';')
        if parce_l[-1] == '':
            parce_l.pop(-1)
        for i in parce_l:
            pre_field = i.strip().split("-")
            field = [a.strip() for a in pre_field]
            if field[0] == 'ProtID':
                self.id = field[1]
            elif field[0] == 'Operon':
                self.operon = field[1]
            elif field[0] == 'Start':
                self.start = int(field[1])
            elif field[0] == 'End':
                self.end = int(field[1])
            elif field[0] == 'Sequence':
                self.seq = field[1]
            elif field[0] == 'Comment':
                self.comment = field[1]           
        

a = ['alpha', 'ProtID - CHU_0183; Operon - 1; Start - 226248; End - 227828; Sequence - MLDVRPDEVSAVLRQQLSNSLTEAQLEEVGTVLQVGDGVARIYGLTKAQAGELLEFEGGLKGMVLNLEEDNVGAVLLGEYSAIKEGSTVKRTKQIAFVNVGEGMVGRVVDTLGNPIDGKGPITGELYKMPMERKAPGVIYRQPVTEPLQTGIKAIDAMIPIGRGQRELIIGDRQTGKTTVALDAIINQKEFYDRGEPVFCIYVACGQKASTIAGIVGTLEKHGAMAYTVVVAATASDPAPMQYFAPFTGAAVGEYFRDTGRPALVVYDDLSKQAVAYREVSLLLRRPPGREAYPGDVFYLHSRLLERAAKINKSDEIAAAMNDLPESLKGIVKGGGSLTALPIIETQAGDVSAYIPTNVISITDGQIFLEINLFNSGVRPAINVGISVSRVGGNAQIKSMKKVAGTLKLDQAQFRELEAFAKFGSDLDASTKLTIERGRRNLEILKQPAFSPVSVEEQVATIYVSTNGFMDSVVVNKVRDFEKDFLTVLRTSHKDTLKEIKSGKIDDAITEVLKKVAKEVAVKYSK; Comments - ;']
d = Subunit_pre(a)
ok = d.pre_check()
d.parce()
print(d.end)


# In[5]:


def parce_file(file_name):
    all_field_list = ['Organism', 'Taxonomy', 'Type', 'Operon number', 'Additional_protein']
    subunit_list = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'A', 'B', 'B1', 'B2', 'C', 'I2']
    f = open(file_name, 'r')
    broken_strings = []
    organisms = []
    org_name_list =[]
    for l in f:
        line = l.strip().split(':')
        if line[0] in all_field_list:
            if line[0] == 'Organism': #The most difficult: how to write info to the correct organism and fof1.
                if len(organisms) != 0:
                    organisms[-1].check()
                    organisms[-1].fof1[-1].check()
                    a = Organism_pre(line)
                    a.parce()
                    if a.name in org_name_list:
                        #print('It doubles')
                        organisms[-1].fof1.append(Atpase_pre())
                    else:
                        organisms.append(a)
                        #temp = organisms[-1].parce()
                        org_name_list.append(organisms[-1].name)
                        organisms[-1].fof1.append(Atpase_pre())
                else:
                    organisms.append(Organism_pre(line))
                    temp = organisms[-1].parce()
                    org_name_list.append(organisms[-1].name)
                    organisms[-1].fof1.append(Atpase_pre())
            elif line[0] == 'Taxonomy':
                organisms[-1].taxonomy = line[1].strip()
            elif line[0] == 'Type':
                t = line[1].strip()
                organisms[-1].fof1[-1].type = t
            elif line[0] == 'Operon number':
                o = int(line[1].strip())
                organisms[-1].fof1[-1].operon_num = o
            elif line[0] == 'Additional_protein':
                organisms[-1].fof1[-1].additional_proteins.append(line[1])
        elif line[0] in subunit_list:
            organisms[-1].fof1[-1].subunits.append(Subunit_pre(line))
            organisms[-1].fof1[-1].subunits[-1].pre_check()
            organisms[-1].fof1[-1].subunits[-1].parce()
            organisms[-1].fof1[-1].subunit_names.append(organisms[-1].fof1[-1].subunits[-1].field_type)
        else:
            broken_strings.append(line)
    organisms[-1].check()
    organisms[-1].fof1[-1].check()

    for i in broken_strings:
        if i != ['']:
            print('Found broken string: {}'.format(i))
    f.close()
    return organisms


# In[6]:


'''organism_list = parce_file('Test_input_ATPase1.txt')
for i in organism_list:
    for k in i.fof1:
        for j in range(int(k.operon_num)):
            for h in k.subunits:
                if int(h.operon) == j+1:
                    print(h.field_type, h.start, h.end)'''

