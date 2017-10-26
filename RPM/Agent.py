# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
# Author: Fardad Hajirostami
# *** DO NOT DISTRIBUTE ***
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import math
import numpy
def initialize(problem):
    A = problem.figures["A"]
    B = problem.figures["B"]
    C = problem.figures["C"]
    _1 = problem.figures["1"]
    _2 = problem.figures["2"]
    _3 = problem.figures["3"]
    _4 = problem.figures["4"]
    _5 = problem.figures["5"]
    _6 = problem.figures["6"]

    figures = [A, B, C]
    solutions = [_1, _2, _3, _4, _5, _6]
    if problem.problemType == "3X3":
        D = problem.figures["D"]
        E = problem.figures["E"]
        F = problem.figures["F"]
        G = problem.figures["G"]
        H = problem.figures["H"]
        _7 = problem.figures["7"]
        _8 = problem.figures["8"]
        figures.extend(D, E, F, G, H)
        solutions.extend(_7, _8)
    return figures, solutions
class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    delDic = {}
    insDic = {}
    sizes_list = ['very small', 'small', 'medium', 'large', 'very large', 'huge']
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def get_all_transforms(self, fig1, fig2, fig3, num):
        transforms = {}
        transforms = self.getSimpleTransforms(fig1, fig2, fig3, transforms, num)
        return transforms
    def getSimpleTransforms(self, fig1, fig2, fig3, transforms, num):
        horizontal = False
        vertical = False
        if (num == 1):
            horizontal = True
        else:
            vertical = True
        deletion = False
        insertion = False
        inversions = {"yes": "no", "no": "yes", "bottom": "top", "top": "bottom",
                "left": "right", "right": "left", "right-half": "left-half",
                "left-half": "right-half" ,"bottom-half": "top-half", "top-half":"bottom-half"}
        insertions = {}
        deletions = {}
        fig1ObjectKeys = sorted(fig1.keys())
        fig2ObjectKeys = sorted(fig2.keys())
        fig3ObjectKeys = sorted(fig3.keys())
        if (len(fig1ObjectKeys) > len(fig2ObjectKeys)):
            deletion = True
        else:
            if (len(fig2ObjectKeys) > len(fig1ObjectKeys)):
                insertion = True
        if (insertion):
            for i in range(len(fig2ObjectKeys)):
                if i > (len(fig1ObjectKeys) - 1):
                    num = int(i) - len(fig1ObjectKeys)
                    insertions[num] = fig2[fig2ObjectKeys[i]]
        deletedObjects = {}
        deletedObs = len(fig1ObjectKeys) - len(fig2ObjectKeys)
        if (deletion):
            for i in range(len(fig1ObjectKeys)):
                fig1_ob = fig1[fig1ObjectKeys[i]]
                fig1_ob["del_prob"] = 0
                deletedObjects[fig1ObjectKeys[i]] = fig1_ob
                for j in range(len(fig2ObjectKeys)):
                    fig2_ob = fig2[fig2ObjectKeys[j]]
                    deletionProb = 1.0
                    if ("angle" in fig1_ob) and ("angle" in fig2_ob):
                        if fig1_ob["angle"] == fig2_ob["angle"]:
                            deletionProb *= .8
                    if ("size" in fig1_ob) and ("size" in fig2_ob):
                        if fig1_ob["size"] == fig2_ob["size"]:
                            deletionProb *= (1 - .08 * math.fabs(self.sizes_list.index(fig1_ob["size"]) - self.sizes_list.index(fig2_ob["size"])))
                    if ("shape" in fig1_ob) and ("shape" in fig2_ob):
                        if fig1_ob["shape"] == fig2_ob["shape"]:
                            deletionProb *= .6
                    if ("fill" in fig1_ob) and ("fill" in fig2_ob):
                        if fig1_ob["fill"] == fig2_ob["fill"]:
                            deletionProb *= .7
                    if ("inside" in fig1_ob) and ("inside" in fig2_ob):
                        if len(fig1_ob["inside"]) == len(fig2_ob["inside"]):
                            deletionProb *= (1 - .02 * math.fabs(len(fig1_ob["inside"]) - len(fig2_ob["inside"])))
                fig1_ob["del_prob"] *= deletionProb
        deletedDic = {}
        for i in range(deletedObs):
            maxDelete = -99999
            maxKey = None
            for key in deletedObjects:
                if deletedObjects[key]["del_prob"] >= maxDelete:
                    maxDelete = deletedObjects[key]["del_prob"]
                    maxKey = key
            deletedDic[maxKey] = deletedObjects.pop(maxKey)
        #print("DELETIONS")
        #print(deletedObjects)
        #print(deletedDic)
        #print("\n\n")
        delMax = {}
        for delKey in deletedDic:
            delOb = deletedDic[delKey]
            for i in range(len(fig3ObjectKeys)):
                fig3_ob = fig3[fig3ObjectKeys[i]]
                deletionProb = 1.0
                if ("angle" in delOb) and ("angle" in fig3_ob):
                    if delOb["angle"] == fig3_ob["angle"]:
                        deletionProb *= .8
                if ("size" in delOb) and ("size" in fig3_ob):
                    if delOb["size"] == fig3_ob["size"]:
                        delta = math.fabs(self.sizes_list.index(delOb["size"]) - self.sizes_list.index(fig3_ob["size"]))
                        size_score = (1 - .08*delta)
                        deletionProb *= size_score
                if ("shape" in delOb) and ("shape" in fig3_ob):
                    if delOb["shape"] == fig3_ob["shape"]:
                        deletionProb *= .6
                if ("fill" in delOb) and ("fill" in fig3_ob):
                    if delOb["fill"] == fig3_ob["fill"]:
                        deletionProb *= .7
                if ("inside" in delOb) and ("inside" in fig3_ob):
                    if len(delOb["inside"]) == len(fig3_ob["inside"]):
                        prob = 1 - .02* math.fabs(len(delOb["inside"]) - len(fig3_ob["inside"]))
                        deletionProb *= prob
                del_score = {}
                del_score[fig3ObjectKeys[i]] = deletionProb
                if delKey not in delMax:
                    delMax[delKey] = del_score
                else:
                    delMax[delKey].update(del_score)
        #print("del maxes")
        #print(delMax)
        fig3_delkeys = []
        for key in delMax:
            currdic = delMax[key]
            minkey = min(currdic, key = currdic.get)
            if (minkey in fig3_delkeys):
                currdic.pop(minkey)
                minkey = min(currdic, key = currdic.get)
            fig3_delkeys.append(minkey)
        #print("keys to Delete!")
        #print(fig3_delkeys)
        #print("ob3 keys before")
        #print(fig3ObjectKeys)
        fig3ObjectKeys = list(set(fig3ObjectKeys) - set(fig3_delkeys))
        #print("after Del")
        #print(fig3ObjectKeys)
        #print("\n")
        object_relationships = {}
        maxO = max(len(fig1ObjectKeys), len(fig2ObjectKeys))
        for i in range(maxO):
            if (i < len(fig1ObjectKeys) and i < len(fig2ObjectKeys)):
                fig_1_ob_att = fig1[fig1ObjectKeys[i]]
                fig_2_ob_att = fig2[fig2ObjectKeys[i]]
                transformations = {}
                if ("angle" in fig_1_ob_att) and ("angle" in fig_2_ob_att):
                    if fig_1_ob_att["angle"] == fig_2_ob_att["angle"]:
                        transformations["angle"] = "same"
                    else:
                        if (horizontal):
                            symmetry_y = self.has_y_symmetry(int(fig_1_ob_att["angle"]), int(fig_2_ob_att["angle"]))
                            #print(symmetry_y)
                            if (symmetry_y):
                                transformations["angle"] = "Y"
                        else:
                            symmetry_x = self.has_x_symmetry(int(fig_1_ob_att["angle"]), int(fig_2_ob_att["angle"]))
                            if (symmetry_x):
                                transformations["angle"] = "X"
                if ("shape" in fig_1_ob_att) and ("shape" in fig_2_ob_att):
                    if fig_1_ob_att["shape"] == fig_2_ob_att["shape"]:
                        transformations["shape"] = "same"
                    else:
                        transformations["shape"] = fig_1_ob_att["shape"] + "," + fig_2_ob_att["shape"]
                if ("size" in fig_1_ob_att) and ("size" in fig_2_ob_att):
                    if fig_1_ob_att["size"] == fig_2_ob_att["size"]:
                        transformations["size"] = "same"
                    else:
                        sizeDelta = self.sizes_list.index(fig_1_ob_att["size"]) - self.sizes_list.index(fig_2_ob_att["size"])
                        transformations["size"] = sizeDelta
                if ("fill" in fig_1_ob_att) and ("fill" in fig_2_ob_att):
                    if fig_1_ob_att["fill"] == fig_2_ob_att["fill"]:
                        transformations["fill"] = "same"
                    else:
                        transformations["fill"] = "inverse"
                if ("alignment" in fig_1_ob_att) and ("alignment" in fig_2_ob_att):
                    if fig_1_ob_att["alignment"] == fig_2_ob_att["alignment"]:
                        transformations["alignment"] = "same"
                    else:
                        fig_1_vertical, fig_1_horizontal = fig_1_ob_att["alignment"].split("-")
                        fig_2_vertical, fig_2_horizontal = fig_2_ob_att["alignment"].split("-")
                        alignChange = ""
                        if (fig_1_vertical != fig_2_vertical):
                            alignChange += "V"
                        if (fig_1_horizontal != fig_2_horizontal):
                            alignChange += "H"
                        transformations["alignment"] = alignChange
                object_relationships[i] = transformations
        solutions = {}
        #print("object relationshipssss")
        #print(object_relationships)
        relationshipKeys = sorted(object_relationships.keys())
        for i in range(len(relationshipKeys)):
            if i < len(fig3ObjectKeys):
                rel_ob_att = object_relationships[relationshipKeys[i]]
                fig_3_ob_att = fig3[fig3ObjectKeys[i]]
                solution = {}
                if ("angle" in fig_3_ob_att) and ("angle" in rel_ob_att):
                    #print("yasss")
                    if rel_ob_att["angle"] == "same":
                        solution["angle"] = fig_3_ob_att["angle"]
                    elif rel_ob_att["angle"] == "Y":
                        if int(fig_3_ob_att["angle"]) <= 90:
                            solution["angle"] = str(90 - int(fig_3_ob_att["angle"]))
                        else:
                            solution["angle"] = str(int(fig_3_ob_att["angle"]) - 90)
                    elif rel_ob_att["angle"] == "X":
                        if int(fig_3_ob_att["angle"]) >= 180:
                            solution["angle"] = str(int(fig_3_ob_att["angle"]) - 90)
                        else:
                            solution["angle"] = str(int(fig_3_ob_att["angle"]) + 90)
                if ("size" in fig_3_ob_att) and ("size" in rel_ob_att):
                    size = fig_3_ob_att["size"]
                    if (rel_ob_att["size"] != "same"):
                        index = rel_ob_att["size"] + self.sizes_list.index(fig_3_ob_att["size"])
                        if (index > (len(self.sizes_list) - 1)):
                            size = self.sizes_list[len(self.sizes_list) - 1]
                        elif (index < 0):
                            size = self.sizes_list[0]
                        else:
                            size = self.sizes_list[index]
                    solution["size"] = size
                if ("shape" in fig_3_ob_att) and ("shape" in rel_ob_att):
                    shape = fig_3_ob_att["shape"]
                    if rel_ob_att["shape"] != "same":
                        shape1, shape2 = rel_ob_att["shape"].split(",")
                        if (shape1 == fig_3_ob_att["shape"]):
                            shape = shape2
                    solution["shape"] = shape
                if ("fill" in fig_3_ob_att) and ("fill" in rel_ob_att):
                    fill = ""
                    if (rel_ob_att["fill"] == "inverse"):
                        if (fig_3_ob_att["fill"] in inversions):
                            fill = inversions[fig_3_ob_att["fill"]]
                    else:
                        fill = fig_3_ob_att["fill"]
                    solution["fill"] = fill
                if ("alignment" in rel_ob_att) and ("alignment" in fig_3_ob_att):
                    vertical, horizontal = fig_3_ob_att["alignment"].split("-")
                    if (rel_ob_att["alignment"] == "VH"):
                        vertical = inversions[vertical]
                        horizontal = inversions[horizontal]
                    elif (rel_ob_att["alignment"] == "V"):
                        vertical = inversions[vertical]
                    elif (rel_ob_att["alignment"] == "H"):
                        horizontal = inversions[horizontal]
                    solution["alignment"] = vertical + "-" + horizontal
                solutions[i] = solution
        return solutions
    def has_y_symmetry(self, angle1, angle2):
        if ((90 - angle1 == angle2 - 90) or (270 - angle1 == angle2 - 270)):
            return True
        else:
            return False
    def has_x_symmetry(self, angle1, angle2):
        if ((180 - angle1 == angle2 - 180) or (360 - angle1 == angle2)):
            return True
        else:
            return False
    def get_score(self,test_sol, solutions):
        #print("test_sol")
        #print(test_sol)
        scores = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for test_key in test_sol:
            test_att = test_sol[test_key]
            for i in range(len(solutions)):
                cand = solutions[i]
                subscoreList = []
                for rav_key in cand:
                    subscore = 1.0
                    rav_ob = cand[rav_key]
                    if ("shape" in rav_ob) and ("shape" in test_att):
                        if (rav_ob["shape"] != test_att["shape"]):
                            subscore *= .4
                    if ("angle" in rav_ob) and ("angle" in test_att):
                        if (rav_ob["angle"] != test_att["angle"]):
                            #print("yass?")
                            subscore *= .5
                    if ("fill" in rav_ob) and ("fill" in test_att):
                        if (rav_ob["fill"] != test_att["fill"]):
                            subscore *= .6
                    if ("alignment" in rav_ob) and ("alignment" in test_att):
                        al_score = 1
                        v, h =  rav_ob["alignment"].split("-")
                        vt, ht = test_att["alignment"].split("-")
                        if (v != vt):
                            al_score -= .2
                        if (h != ht):
                            al_score -= .2
                        subscore *= al_score
                    if ("size" in rav_ob) and ("size" in test_att):
                        delta = math.fabs(self.sizes_list.index(rav_ob["size"]) - self.sizes_list.index(test_att["size"]))
                        size_score = (1 - .08*delta)
                        subscore *= size_score
                    sizeDiff = (1 - .1 * math.fabs(len(cand) - len(test_sol)))
                    subscore *= sizeDiff
                    subscoreList.append(subscore)
                #print(i)
                #print("subscore", subscore)
                scores[i] += max(subscoreList)
        return scores
    def Solve(self,problem):
        print("problem name ", problem.name)
        print("Challenge Problem C" in problem.name)
        figures, solutions = initialize(problem)
        A_att = {}
        B_att = {}
        C_att = {}
        D_att = {}
        E_att = {}
        F_att = {}
        G_att = {}
        H_att = {}
        _1_att = {}
        _2_att = {}
        _3_att = {}
        _4_att = {}
        _5_att = {}
        _6_att = {}
        _7_att = {}
        _8_att = {}
        for figure in figures:
            for ravenOb in figure.objects:
                #print(ravenOb)
                #print(figure.objects[ravenOb].attributes)
                name = figure.objects[ravenOb].name
                if (figure.name == 'A'):
                    A_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'B'):
                    B_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'C'):
                    C_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'D'):
                    A_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'E'):
                    B_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'F'):
                    C_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'G'):
                    A_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'H'):
                    B_att[name] = figure.objects[ravenOb].attributes

            #fAtt[figure.name] = figure.objects.values()[0].attributes
        for solution in solutions:
            for ravenObs in solution.objects:
                name = solution.objects[ravenObs].name
                if (solution.name == '1'):
                    _1_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '2'):
                    _2_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '3'):
                    _3_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '4'):
                    _4_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '5'):
                    _5_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '6'):
                    _6_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '7'):
                    _6_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '8'):
                    _6_att[name] = solution.objects[ravenObs].attributes
        score = 3
        if ("B-" in problem.name):
            solutions = [ _1_att, _2_att, _3_att, _4_att, _5_att, _6_att]
            transforms = {}
            gen_sol = self.get_all_transforms(A_att, B_att, C_att, 1)
            gen_sol2 = self.get_all_transforms(A_att, C_att, B_att, 0)
            scores = self.get_score(gen_sol, solutions)
            scores2 = self.get_score(gen_sol2, solutions)
            sum_score_1 = float(numpy.sum(scores))
            sum_score_2 = float(numpy.sum(scores2))
            formatted_list = []
            formatted_list2 = []
            formatted_list3 = []
            if (sum_score_1 > 0):
                scores = [x/sum_score_1 for x in scores]
                for item in scores:
                    formatted_list.append("%.3f"%item)
            if (sum_score_2 > 0):
                scores2 = [x/sum_score_2 for x in scores2]
                for item in scores2:
                    formatted_list2.append("%.3f"%item)
            finalScore = [0, 0, 0, 0, 0, 0]
            for i in range(len(finalScore)):
                finalScore[i] = scores[i] * scores2[i]
            for item in finalScore:
                formatted_list3.append("%.3f"%item)
            score = finalScore.index(max(finalScore)) + 1
            #scores = [a*b for a,b in zip(scores,scores2)]
            #print("A -> B")
            #print("solution horizontal", gen_sol2)
            #print("A -> C")
            #print("solution vertical", gen_sol)
            #print("\n")
            #print("scores: A -> B", formatted_list)
            #print("scores: A -> C", formatted_list2)
            print("FINAL SCORE")
            #print(formatted_list3)
            print(score)
            print("\n\n")
        elif ("C-" in problem.name):
            print("here CCCC")
        #print("\n\n\n\n\n\n\n")
        """
        print(gen_sol)
        print(solutions[1])
        print("\n")
        print(A_att)
        print("\n")
        print(B_att)
        print("\n")
        print(C_att)
        #print(sAtt)
        """
        """
        for figure in problem.figures:
            ravensfigure = problem.figures.get(figure)
            print(ravensfigure.name)
            ravensObject = ravensfigure.objects.values()
            print(ravensObject[0].attributes)
        """
        return score

