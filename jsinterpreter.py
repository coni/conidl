import re

class coninterpreter:
    # C'est de la copie, plutot une interpretation du code d'origine selon comment je l'ai compris.
    # J'ai essayer de simplifier pour comprendre plus facilement :) je suis content du resultat pour mon niveau

    def __init__(self, code):
        self.code = code
        self.variable = {}
    

    def execute_code(self, code):

    # RETURN 
        r_code = re.search(r"return (?P<result>.*)",code)
        if r_code:
            return self.execute_code(r_code.group("result"))

        
    
    #  ATTRIBUTION DE VARIABLE
        r_code = re.search(r"(var\s)?(?P<var>([a-zA-Z0-9]*))(\[(?P<index>.+)\])?=(?P<result>.+)",code)
        if r_code:
            index = r_code.group("index")
            if r_code.group("index") == None:
                self.variable[r_code.group("var")] = self.execute_code(r_code.group("result"))
            else:
                if index.isdigit() == True:
                    index = int(index)
                else:
                    index = self.execute_code(index)
                self.variable[r_code.group("var")][index] = self.execute_code(r_code.group("result"))
              
            return None
    
    #  a.Length
        r_code = re.search(r"(^)(?P<obj>[\w\d]+)\.length", code)
        if r_code:
            if r_code.group("obj") in self.variable:
                return len(self.variable[r_code.group("obj")])


    # CHERCHE FONCTION
        r_code = re.search(r"(?P<obj>[\w\d]+)\.(?P<member>[\w\d]*)\((?P<member_args>.*)\)", code)
        if r_code:
            
            if r_code.group("obj") in self.variable:
                if r_code.group("member") == "split":
                    if r_code.group("member_args") == '""':
                        return list(self.variable[r_code.group("obj")])

                if r_code.group("member") == "reverse":
                    return self.variable[r_code.group("obj")].reverse()

                if r_code.group("member") == "join":
                    return "".join(self.variable[r_code.group("obj")])

                

                """ A FAIRE"""
                if r_code.group("member") == "splice":
                    if r_code.group("member_args") != None:
                        arg = r_code.group("member_args").split(",")
                        for i in range(len(arg)):
                            if arg[i].isdigit() == True:
                                arg[i] = int(arg[i])
                            else:
                                arg[i] = self.execute_code(arg[i])

                    if r_code.group("obj") in self.variable:
                        res = []
                        for i in range(arg[0], min(arg[0] + arg[1], len(self.variable[r_code.group("obj")]))):
                            res.append(self.variable[r_code.group("obj")].pop(arg[0]))
                        return res
                        
                """ A FAIRE"""

            else:
    # OBJET
                return self.find_object(r_code)

    # VARIABLE & INDEX
        r_code = re.search(r"(^)(?P<var>[a-zA-Z0-9]+)(\[(?P<index>.+)\])?$", code)
        if r_code:
            
            if r_code.group("index") == None:
                return self.variable[r_code.group("var")]
            else:
                if r_code.group("index").isdigit():
                    index = int(r_code.group("index"))
                else:
                    index = self.execute_code(r_code.group("index"))
                return self.variable[r_code.group("var")][index]

    # OPERATOR
        r_code = re.search(r"(?P<member_1>.*)(?P<operator>[\%\+\-\*\/])(?P<member_2>.+)", code)
        if r_code:
            member_1 = r_code.group("member_1")
            member_2 = r_code.group("member_2")
            if member_1.isdigit() == False:
                if member_1 in self.variable:
                    if type(self.variable[member_1]) == int:
                        member_1 = self.variable[member_1]
                    else:
                        print("probleme %s n'est pas un digit" % (self.variable[member_1]))
                        exit()
                else:
                    member_1 = self.execute_code(member_1)
            
            if member_2.isdigit() == False:
                if member_2 in self.variable:
                    if type(self.variable[member_2]) == int:
                        member_2 = self.variable[member_2]
                    else:
                        print("probleme %s n'est pas un digit" % (self.variable[member_2]))
                        exit()
                else:
                    member_2 = self.execute_code(member_2)

            if r_code.group("operator") == "+":
                return member_1 + member_2
            elif r_code.group("operator") == "-":
                return member_1 - member_2
            elif r_code.group("operator") == "*":
                return member_1 * member_2
            elif r_code.group("operator") == "/":
                return member_1 / member_2
            elif r_code.group("operator") == "%":
                return member_1 % member_2


    def execute_function(self, funcname, args):
        main_expression = re.search(r"(?P<funcname>%s)=function\((?P<args>[\s\S]{1,10})\)\{(?P<code>.*?)\}" % (funcname), self.code)
        self.variable[main_expression.group("args")] = args
        for code in main_expression.group("code").split(";"):
            resultat = self.execute_code(code)
        return resultat


    def find_object(self, r_code):

        _FUNC_NAME_RE = r'''(?:[a-zA-Z$0-9]+|"[a-zA-Z$0-9]+"|'[a-zA-Z$0-9]+')'''
        obj = {}
        obj_m = re.search(
            r'''(?x)
                (?<!this\.)%s\s*=\s*{\s*
                    (?P<fields>(%s\s*:\s*function\s*\(.*?\)\s*{.*?}(?:,\s*)?)*)
                }\s*;
            ''' % (re.escape(r_code.group("obj")), _FUNC_NAME_RE),
            self.code)

        if obj_m:
            for code in obj_m.group("fields").splitlines():
                object_func = re.search(r"%s:function\((?P<args>[\s\S]*)\)\{(?P<code>(.*?))\}" % (r_code.group("member")), code)
                if object_func:
                    # Attribution des Variables
                    for index in range(len(object_func.group("args").split(","))):
                        if r_code.group("member_args").split(",")[index].isdigit():
                            self.variable[object_func.group("args").split(",")[index]] = int(r_code.group("member_args").split(",")[index])
                    for code in object_func.group("code").split(";"):
                        self.execute_code(code)
        return None