import sys

################################
######## CLASS OBJECTS #########
################################

class Lexeme:
    def __init__(self, n, c = None, v: float = None) :
        self.nature = n
        self.chaine = c
        self.val:float = v

class Lexeme_liste:
    def __init__(self, liste = None) :
        self.liste = liste
        self.pos = 0

    def est_vide(self):
        return self.pos >= len(self.liste)

    def lexeme_en_cours(self):
        return self.liste[self.pos]
    
    def nature_en_cours(self):
        return self.liste[self.pos].nature

    def avancer(self):
        self.pos += 1

################################
###### LEXICAL ANALYSIS ########
################################

def lexical_analysis(s) :
    lexeme_list = []
    etat = "classic"
    i = 0
    chaine = ""
    while i < len(s):
        if etat == "classic":
            if s[i] == "(":
                lexeme_list.append(Lexeme("PARO","("))
                i += 1 

            elif s[i] == ")":
                lexeme_list.append(Lexeme("PARF",")"))
                i += 1 

            elif s[i] == "{":
                lexeme_list.append(Lexeme("ACCO","{"))
                i += 1 

            elif s[i] == "}":
                lexeme_list.append(Lexeme("ACCF","}"))
                i += 1 

            elif s[i] == "[":
                lexeme_list.append(Lexeme("CROO","["))
                i += 1

            elif s[i] == "]":
                lexeme_list.append(Lexeme("CROF","]"))
                i += 1

            elif s[i] == ",":
                lexeme_list.append(Lexeme("VIRG",","))
                i += 1

            elif s[i] == "?":
                lexeme_list.append(Lexeme("QUEST","?"))
                i += 1

            elif s[i] == ".":
                lexeme_list.append(Lexeme("DOT","."))
                i += 1

            elif s[i] == "+":
                lexeme_list.append(Lexeme("PLUS","+"))
                i += 1

            elif s[i] == "*":
                lexeme_list.append(Lexeme("STAR","*"))
                i += 1

            elif s[i] == "|":
                lexeme_list.append(Lexeme("OR","|"))
                i += 1

            elif ord("0") <= ord(s[i]) <= ord("9"):
                entier = s[i]
                i += 1
                etat = "entier"

            elif s[i] == " ":
                i += 1 

            elif s[i] == "\\":
                i += 1
                etat = "special"

            else:
                lexeme_list.append(Lexeme("CHAR",s[i]))
                i += 1

        elif etat == "entier":
            if ord("0") <= ord(s[i]) <= ord("9"):
                entier += s[i]
                i += 1
            else:
                lexeme_list.append(Lexeme("INT",entier,int(entier)))
                etat = "classic"
        
        elif etat == "special":
            lexeme_list.append(Lexeme("CHAR",s[i]))
            i += 1
            etat = "classic"

            
    lexeme_list.append(Lexeme("END",""))
    return Lexeme_liste(lexeme_list)

################################
###### SYNTAXIC ANALYSIS #######
################################

def syntaxic_analysis(L) :
    return regex(L)

def regex(L):
    if L.nature_en_cours() == "END":
        return ""
    return seq_re(L)

def seq_re(L,par_open=False) :
    if L.nature_en_cours() == "END":
        print('Error : empty sequence')
        exit()
    repet = pre_op(L)
    s = re(L)    
    s_op = post_op(L,s)
    res = "" 
    for x in range(repet[0]):
        res += s_op
    for x in range(repet[1] - repet[0]):
        res += "(" + s_op + "+e)"
    return res + suite_seq_re(L,par_open)

def suite_seq_re(L,par_open=False) :
    if L.nature_en_cours() == "END" or (L.nature_en_cours() == "PARF" and par_open):
        return ""
    repet = pre_op(L)
    s = re(L)    
    s_op = post_op(L,s)
    res = "" 
    for x in range(repet[0]):
        res += s_op
    for x in range(repet[1] - repet[0]):
        res += "(" + s_op + "+e)"
    return res + suite_seq_re(L,par_open)


def pre_op(L):
    if L.nature_en_cours() == "ACCO":
        L.avancer()
        if L.nature_en_cours() == "INT":
            m = L.lexeme_en_cours().val
            L.avancer()
        else:
            print("Error : Need an INT after {")
            exit()
        n = repet(L)
        if n == 0:
            return (m,m)
        elif n < m:
            print("Error : n cannot be inferior to m in {m,n}")
            exit()
        else:
            return (m,n)
    else:
        return (1,1)

def post_op(L,s) :
    if L.nature_en_cours() == "OR":
        L.avancer()
        return "(" + s + "+" + re(L) + ")"
    elif L.nature_en_cours() == "STAR":
        L.avancer()
        return s + "*"
    elif L.nature_en_cours() == "PLUS":
        L.avancer()
        return s + "\+"
    elif L.nature_en_cours() == "QUEST":
        L.avancer()
        return "(" + s + "+e)"
    else:
        return s


def re(L) :
    s = ""
    if L.nature_en_cours() == "CROO":
        L.avancer()
        c = chaine(L)
        if L.nature_en_cours() != "CROF":
            print("Error : Need a ] after [abc")
            exit()
        else:
            L.avancer()
            s = "("
            for i in range(len(c) - 1):
                s += c[i] + "+"
            s += c[-1] + ")"
            return s

    elif L.nature_en_cours() == "PARO":
        L.avancer()
        s = "(" + seq_re(L,True) + ")"
        L.avancer()
        return s
    
    elif L.nature_en_cours() == "CHAR":
        s = L.lexeme_en_cours().chaine
        L.avancer()
        return s 
    
    elif L.nature_en_cours() == "INT":
        s = L.lexeme_en_cours().chaine
        L.avancer()
        return s

    elif L.nature_en_cours() == "DOT":
        L.avancer()
        return "E"

    else:
        print("Error : unexcepted char")
        exit()

def repet(L) :
    if L.nature_en_cours() == "VIRG":
        L.avancer()
        if L.nature_en_cours() == "INT":
            n = L.lexeme_en_cours().val
            L.avancer()
            if L.nature_en_cours() == "ACCF":
                L.avancer()
                return n
            else:
                print("Error : Need an } to close {m,n")
                exit()
        else:
            print("Error : Need an INT after ,")
            exit()
    elif L.nature_en_cours() == "ACCF":
            L.avancer()
            return 0
    else:
        print("Error : Need an INT or , after {m")
        exit()


def chaine(L) :
    if L.nature_en_cours() == "CHAR" or L.nature_en_cours() == "INT":
        s = L.lexeme_en_cours().chaine
        L.avancer() 
        return s + suite_chaine(L)
    else:
        print("Error : CHAR needed")
        exit()

def suite_chaine(L) :
    if L.nature_en_cours() == "CHAR" or L.nature_en_cours() == "INT":
        s = L.lexeme_en_cours().chaine
        L.avancer() 
        return s + suite_chaine(L)
    else:
        return ""








################################
############ MAIN ##############
################################

def regex_to_classic_re(regex) :
    """Lexical analys, follow by syntaxic analysis to return a Classic RE"""
    L = lexical_analysis(regex)
    return syntaxic_analysis(L)



s = ""
for pos,x in enumerate(sys.argv):
    if pos != 0:
        s += x
print(regex_to_classic_re(s))

