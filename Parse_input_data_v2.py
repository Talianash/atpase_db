
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

# ### Версия 2
# Эта версия исправлена для файла Operons_formatted_231018.txt, который Таня прислала 23.10.18. 
# 
# 1)в файле появились строки, состоящие из "-----", надо ввести для них исключение, как для пустых (+)
# 
# 2)вместо идентификатора "Type" используется идентификатор "ATP synthase type" (+)
# 
# 3)пропало поле operon number, появилось поле operon type - пока просто добавлю его, на старое поле поставила счетчик (+)
# 
# 4)появился блок с перечислением субъединиц и их поличествами, выглядит как мини-табличка. Думаю, скрипт должен его игнорировать (+/-)
# 
# 5)из строки про последовательность было убрано поле Operon, зато появились поля Length и Direction (+)
# 
# Добавила обратные ссылки, теперть по последовательности можно восстановить фермент, по ферменту можно восстановить организм.
# 
# Еще надо изменить схему, как АТФ-синтазы добавляются в организмы.

# In[40]:


class Organism_pre(object):
    def __init__(self, list_1):
        self.field_type = list_1[0] 
        self.field_info = list_1[1] #second part of the line, where name and id are stated
        self.warnings = [] #V2_added, to check if the organism should be added to the database
        self.name = ''
        self.id = ''
        self.taxonomy = ''
        self.operon_num = 0 #V2_added
        self.fof1 = [] # Atpase_pre objects are added here
        
    def add_operon_num(self): #V2_added
        for i in self.fof1:
            self.operon_num = self.operon_num + i.operon_num
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
            print('-----------------------' + self.name + '-----------------------')
            print('\n'.join(warnings))
        return 0
        
    def parce(self):
        parce_l = self.field_info.strip().split()
        self.name = parce_l.pop(0) + ' ' + parce_l.pop(0)
        self.id = ' '.join(parce_l)
        return 0


# In[41]:


class Atpase_pre(object):
    def __init__(self):
        organism = 0
        self.type = ''
        self.operon_num = 0
        self.operon_type = [] #V2_Added!!
        self.subunit_names = []
        self.subunits = [] #Subunit_pre objects are added here
        self.additional_proteins = [] #
        self.field_list = ['Organism', 'Taxonomy', 'Type', 'Operon number', 'Additional_protein']
        self.subunit_list = [['alpha'], ['beta'], ['gamma'], ['delta'], ['epsilon'], ['A'], ['B', 'B1', 'B2'], ['C'], ['I2', 'I']] #V2_Changed!! I added
        
    def check(self):
        warnings = []
        happy_messages = []
        if self.type == '':
            warn1 = 'Warning! FoF1 type is not stated'
            warnings.append(warn1)
            self.organism.warnings.append(warn1)
            #print(self.organism.warnings)
        if self.operon_num == 0:
            warn2 = 'Warning! Operon number is not stated'
            warnings.append(warn2)
            self.organism.warnings.append(warn2)
            #print(self.organism.warnings)
        if self.subunits == []:
            warn3 = 'Warning! No subunits found'
            warnings.append(warn3)
            self.organism.warnings.append(warn3)
            #print(self.organism.warnings)
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
            warn4 = 'Warning! Subunit names are not stated'
            warnings.append(warn4)
            self.organism.warnings.append(warn4)
        if warnings == []:
            happy_messages.append('We checked {}, everything is fine. Additional proteins: {}'.format(self.type, len(self.additional_proteins)))
            happy_messages.reverse()
            #print('. '.join(happy_messages))
        else:
            print('-----------------------' + self.organism.name + '-----------------------')
            print('\n'.join(warnings))
        return 0


# In[ ]:


class Operon(object):
    def __init__(self):
        self.number = 0
        self.subunits = []


# In[42]:


class Subunit_pre(object):
    def __init__(self, list_1):
        self.field_type = list_1[0]
        self.field_info = list_1[1]
        self.atpase = 0
        self.id = ''
        self.operon = 0
        self.start = 0
        self.end = 0
        self.length = 0 #V2_added!!
        self.direction = '' #V2_added!!
        self.seq = ''
        self.comment = ''
        self.field_list = ['ProtID', 'Start', 'End', 'Sequence', 'Comments', 'Length', 'Direction'] #V2_changed!! Operon field deleted, Length and Direction were added
        self.field_check = ['No', 'No', 'No', 'No', 'No', 'No', 'No']
    
    
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
            elif field[0] == 'Length': #V2_added!!
                self.length = int(field[1])
            elif field[0] == 'Direction': #V2_added!! VERY DIRTY SOLUTION
                if len(field) == 3:
                    self.direction = '-1'
                elif len(field) == 2:
                    self.direction = '1'
            elif field[0] == 'Start':
                self.start = int(field[1])
            elif field[0] == 'End':
                self.end = int(field[1])
            elif field[0] == 'Sequence':
                self.seq = field[1]
            elif field[0] == 'Comment':
                self.comment = field[1]           
        

a = ['beta', 'ProtID - AM1_D0157; Start - 123957; End - 125327; Length - 1370; Direction - -1; Sequence - MVDVHFSDEVPPLRHLLRAGPQAQIAIEGLTYLSANLIRGIALTPTQGLARGARVIDTGQSLQVPIGEHLLGRAFNVFGDPIDGLGPLKGMKRSLHGQAVPLHQRTTGTDILVTGIKAIDLLAPLERGSKAGLFGGAGVGKTVLITEMIHNIVSRYDGVSIFCGIGERSREGEELYREMKAAGVLNNTVMVFGQMNEPPGSRFRVGHAALTMAEYFRDQAHRDVLLMIDNVFRFIQAGSEVSGLMGQLPSRVGYQPTLATELAELEERICSTAHGAITSVQAVYIPADDLTDPAAVHTFSHLSASIVLSRKRTSEGLYPAVDPLQSGSKMLTPSVVGQRHYQVAQAVRKTLAEYEDLKDIIAMLGLEELAQNERQTVYRARRLERFLTQPFFTTEQFSGIPGKMVSLDQTLTGCEAILDDKCSGLSEQALYMIGAVDEAELEHQEREAQEVEEIGQ; Comments - ;']
d = Subunit_pre(a)
ok = d.pre_check()
d.parce()
print(d.direction)


# In[67]:


def parce_file(file_name):
    all_field_list = ['Organism', 'Taxonomy', 'ATP synthase type', 'Operon number', 'Operon type', 'Additional_protein'] #V2_changed!! Type is changed to 'ATP synthase type', 'Operon type' added
    subunit_list = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'A', 'B', 'B1', 'B2', 'C', 'I2', 'I']
    f = open(file_name, 'r')
    broken_strings = []
    organisms = []
    broken_organisms = []
    org_name_list =[]
    for l in f:
        line = l.strip().split(':')
        if line[0] in all_field_list:
            if line[0] == 'Organism': #The most difficult: how to write info to the correct organism and fof1.
                if len(organisms) != 0:
                    organisms[-1].check()
                    organisms[-1].add_operon_num()
                    if len(organisms[-1].fof1) != 0:
                        organisms[-1].fof1[-1].check()
                    a = Organism_pre(line)
                    a.parce()
                    if a.name in org_name_list:
                        #print('It doubles')
                        #organisms[-1].fof1.append(Atpase_pre())
                        #organisms[-1].fof1[-1].organism = organisms[-1]
                        meme = 0
                    else:
                        organisms.append(a)
                        #temp = organisms[-1].parce()
                        org_name_list.append(organisms[-1].name)
                        #organisms[-1].fof1.append(Atpase_pre())
                        #organisms[-1].fof1[-1].organism = organisms[-1]
                else:
                    organisms.append(Organism_pre(line))
                    temp = organisms[-1].parce()
                    org_name_list.append(organisms[-1].name)
                    #organisms[-1].fof1.append(Atpase_pre())
                    #organisms[-1].fof1[-1].organism = organisms[-1]
            elif line[0] == 'Taxonomy':
                organisms[-1].taxonomy = line[1].strip()
            elif line[0] == 'ATP synthase type':
                print(organisms[-1].name)
                organisms[-1].fof1.append(Atpase_pre())
                organisms[-1].fof1[-1].organism = organisms[-1]
                t = line[1].strip()
                organisms[-1].fof1[-1].type = t
            elif line[0] == 'Operon type':#V2_changed!! It was 'Operon number' but now it will be just calculated
                organisms[-1].fof1[-1].operon_num = organisms[-1].fof1[-1].operon_num + 1 #V2!
                o = line[1].strip() #V2!
                organisms[-1].fof1[-1].operon_type.append(o) #V2
            elif line[0] == 'Additional_protein':
                organisms[-1].fof1[-1].additional_proteins.append(line[1])
        elif line[0] in subunit_list:
            organisms[-1].fof1[-1].subunits.append(Subunit_pre(line))
            organisms[-1].fof1[-1].subunits[-1].atpase = organisms[-1].fof1[-1]
            organisms[-1].fof1[-1].subunits[-1].operon = len(organisms[-1].fof1[-1].operon_type)
            organisms[-1].fof1[-1].subunits[-1].pre_check()
            organisms[-1].fof1[-1].subunits[-1].parce()
            organisms[-1].fof1[-1].subunit_names.append(organisms[-1].fof1[-1].subunits[-1].field_type)
        else:
            broken_strings.append(line)
    organisms[-1].check()
    organisms[-1].fof1[-1].check() #V2_changed!!

    for i in broken_strings:
        if i != [''] and i != ['---------------'] and i != ['a\tb\tg\td\te\tA\tB\tB1\tB2\tC\tI\tI2'] and i[0][1:2] != '\t':
            print('Found broken string: {}'.format(i))
    f.close()
    return organisms, broken_organisms




