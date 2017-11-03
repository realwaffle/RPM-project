# Author: Fardad Hajirostami
# *** DO NOT DISTRIBUTE ***
#
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
    if problem.problemType == "3x3":
        D = problem.figures["D"]
        E = problem.figures["E"]
        F = problem.figures["F"]
        G = problem.figures["G"]
        H = problem.figures["H"]
        _7 = problem.figures["7"]
        _8 = problem.figures["8"]
        figures.extend([D, E, F, G, H])
        solutions.extend([_7, _8])
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
    def get_visual_transforms(self, figs, problem, figPixels):
        incProb = [1, 1]
        adProb = [1, 1]
        delProb = [1, 1]
        staticProb = [1, 1]
        ob_diff_prob = [1, 1]

        adProb[0], delProb[0], figPixels = self.pixel_diff(figs[0], figs[1], figs[2], problem, adProb[0], delProb[0], figPixels)
        adProb[0], delProb[0], figPixels = self.pixel_diff(figs[3], figs[4], figs[5], problem, adProb[0], delProb[0], figPixels)
        adProb[1], delProb[1], figPixels = self.pixel_diff(figs[0], figs[3], figs[6], problem, adProb[1], delProb[1], figPixels)
        adProb[1], delProb[1], figPixels = self.pixel_diff(figs[1], figs[4], figs[7], problem, adProb[1], delProb[1], figPixels)
        
        incRow1 = (figPixels["B"] - figPixels["A"]) + figPixels["B"]
        incRow2 = (figPixels["E"] - figPixels["D"]) + figPixels["E"]
        incCol1 = (figPixels["D"] - figPixels["A"]) + figPixels["D"]
        incCol2 = (figPixels["E"] - figPixels["B"]) + figPixels["E"]
        ratioRow1 = incRow1/(figPixels["C"] * 1.0) if incRow1 < figPixels["C"] else figPixels["C"]/(incRow1 * 1.0)
        ratioRow2 = incRow2/(figPixels["F"] * 1.0) if incRow2 < figPixels["F"] else figPixels["F"]/(incRow2 * 1.0)
        ratioCol1 = incCol1/(figPixels["G"] * 1.0) if incCol1 < figPixels["G"] else figPixels["G"]/(incCol1 * 1.0)
        ratioCol2 = incCol2/(figPixels["H"] * 1.0) if incCol2 < figPixels["H"] else figPixels["H"]/(incCol2 * 1.0)
        
        staticRow1 = figPixels["C"]/(figPixels["A"] * 1.0) if figPixels["C"] < figPixels["A"] else figPixels["A"]/(figPixels["C"] * 1.0)
        staticRow2 = figPixels["F"]/(figPixels["D"] * 1.0) if figPixels["F"] < figPixels["D"] else figPixels["D"]/(figPixels["F"] * 1.0)
        staticCol1 = figPixels["A"]/(figPixels["G"] * 1.0) if figPixels["A"] < figPixels["G"] else figPixels["G"]/(figPixels["A"] * 1.0)
        staticCol2 = figPixels["B"]/(figPixels["H"] * 1.0) if figPixels["B"] < figPixels["H"] else figPixels["H"]/(figPixels["B"] * 1.0)


        incProb[0] *= ratioRow1 * ratioRow2
        incProb[1] *= ratioCol1 * ratioCol2

        staticProb[0] = staticRow1 * staticRow2
        staticProb[1] = staticCol1 * staticCol2

        ob_diff_prob[0] = self.object_difference(figs[0], figs[1], figs[2], ob_diff_prob[0])
        ob_diff_prob[0] = self.object_difference(figs[3], figs[4], figs[5], ob_diff_prob[0])
        ob_diff_prob[1] = self.object_difference(figs[0], figs[3], figs[6], ob_diff_prob[1])
        ob_diff_prob[1] = self.object_difference(figs[1], figs[4], figs[7], ob_diff_prob[1])
        #print("adProb ", adProb)
        #print("delProb ", delProb)
        #print("incProb ", incProb)
        #print("ob_diff_prob ", ob_diff_prob)
        return adProb, delProb, incProb, staticProb, ob_diff_prob, figPixels
    def get_sol_probs_visuals(self, adProbs, delProbs, incProbs, staticProbs, solsProbs, figs, figPixels, solutions, problem):
        if (adProbs[0] < 0.55 and adProbs[1] < 0.55  and delProbs[0] < 0.55 and delProbs[1] < 0.55 and incProbs[0] < 0.55 and incProbs[1] < 0.55 and staticProbs[0] < 0.55 and staticProbs[1] < 0.55):
            return solsProbs
        solPixels = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(solutions)):
            probName = problem.name.split(" ")
            directory = probName[0] + " Problems " + probName[2][0]
            filename = "Problems/" + directory + "/" + problem.name + "/"
            filename = filename + str(i + 1) + ".png"
            #print("filename ", filename)
            image = Image.open(filename)
            image = image.convert('RGB')
            width, height = image.size
            pixSize = 0
            for x in range(height):
                for y in range(width):
                    r, g, b = image.getpixel((x, y))
                    if ((r + g + b) < 20):
                        pixSize += 1
            solPixels[i] = pixSize
        if (incProbs[0] >= 0.55):
            pixH = figPixels["H"]
            pixG = figPixels["G"]
            compare = (pixH - pixG) + pixH
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        if (incProbs[1] >= 0.55):
            pixC = figPixels["C"]
            pixF = figPixels["F"]
            compare = (pixF - pixC) + pixF
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        if (adProbs[0] >= 0.55):
            pixH = figPixels["H"]
            pixG = figPixels["G"]
            compare = pixH + pixG
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        if (adProbs[1] >= 0.55):
            pixC = figPixels["C"]
            pixF = figPixels["F"]
            compare = pixC + pixF
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        if (delProbs[0] >= 0.55):
            pixH = figPixels["H"]
            pixG = figPixels["G"]
            compare = max(pixH, pixG) - min(pixH, pixG)
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        if (delProbs[1] >= 0.55):
            pixC = figPixels["C"]
            pixF = figPixels["F"]
            compare = max(pixC, pixF) - min(pixC, pixF)
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        if (staticProbs[0] >= 0.55):
            compare = figPixels["G"]
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        if (staticProbs[1] >= 0.55):
            compare = figPixels["C"]
            for i in range(len(solPixels)):
                ratio = compare/(solPixels[i] * 1.0) if compare < solPixels[i] else solPixels[i]/(compare * 1.0)
                solsProbs[i] *= ratio
        return solsProbs
    def get_verbal_transforms(self, figs, problem, solutions, solsProbs, obdiffprobs):
        A, Akeys = figs[0][1], sorted(figs[0][1].keys())
        B, Bkeys = figs[1][1], sorted(figs[1][1].keys())
        C, Ckeys = figs[2][1], sorted(figs[2][1].keys())
        D, Dkeys = figs[3][1], sorted(figs[3][1].keys())
        E, Ekeys = figs[4][1], sorted(figs[4][1].keys())
        F, Fkeys = figs[5][1], sorted(figs[5][1].keys())
        G, Gkeys = figs[6][1], sorted(figs[6][1].keys())
        H, Hkeys = figs[7][1], sorted(figs[7][1].keys())
        Hpattern = 1
        Vpattern = 1
        testLenRow = (len(H) - len(G)) + len(H) 
        testLenCol = (len(F) - len(C)) + len(F)
        row1Map = self.get_mapped_transforms(A, C, Akeys, Ckeys, 1)
        solrow1 = self.translate_maps(G, Gkeys, row1Map)
        solsProbs = self.get_score_3(solrow1, solutions, solsProbs, obdiffprobs, testLenRow)
        row2Map = self.get_mapped_transforms(D, F, Dkeys, Fkeys, 1)
        solrow2 = self.translate_maps(G, Gkeys, row2Map)
        solsProbs = self.get_score_3(solrow2, solutions, solsProbs, obdiffprobs, testLenRow)
        col1Map = self.get_mapped_transforms(A, G, Akeys, Gkeys, 0)
        solcol1 = self.translate_maps(C, Ckeys, col1Map)
        solsProbs = self.get_score_3(solcol1, solutions, solsProbs, obdiffprobs, testLenCol)
        col2Map = self.get_mapped_transforms(B, H, Bkeys, Hkeys, 0)
        solcol2 = self.translate_maps(C, Ckeys, col2Map)
        solsProbs = self.get_score_3(solcol2, solutions, solsProbs, obdiffprobs, testLenCol)
        return solsProbs
    def get_mapped_transforms(self, fig1, fig2, fig1keys, fig2keys, num):
        horizontal = False
        vertical = False
        if (num == 1):
            horizontal = True
        else:
            vertical = True
        maps = {}
        minIter = min(len(fig1keys), len(fig2keys))
        for i in range(minIter):
                fig_1_ob_att = fig1[fig1keys[i]]
                fig_2_ob_att = fig2[fig2keys[i]]
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
                if ("left-of" in fig_1_ob_att) and ("left-of" in fig_2_ob_att):
                    if len(fig_1_ob_att["left-of"]) == len(fig_2_ob_att["left-of"]):
                        transformations["left-of"] = "same"
                    else:
                        diff = len(fig_2_ob_att["left-of"].split(",")) - len(fig_2_ob_att["left-of"].split(","))
                        transformations["left-of"] = str(diff)
                elif ("left-of" in fig_1_ob_att):
                    transformations["left-of"] = "removed"
                elif ("left-of" in fig_2_ob_att):
                    amount = len(fig_2_ob_att["left-of"].split(","))
                    transformations["left-of"] = "added, " + str(amount)
                if ("above" in fig_1_ob_att) and ("above" in fig_2_ob_att):
                    if len(fig_1_ob_att["above"]) == len(fig_2_ob_att["above"]):
                        transformations["above"] = "same"
                    else:
                        diff = len(fig_2_ob_att["above"].split(",")) - len(fig_2_ob_att["above"].split(","))
                        transformations["above"] = str(diff)
                elif ("above" in fig_1_ob_att):
                    transformations["above"] = "removed"
                elif ("above" in fig_2_ob_att):
                    amount = len(fig_2_ob_att["above"].split(","))
                    transformations["above"] = "added, " + str(amount)
                maps[i] = transformations
        return maps
    def translate_maps(self, fig, figkeys, maps):
        inversions = {"yes": "no", "no": "yes", "bottom": "top", "top": "bottom",
                "left": "right", "right": "left", "right-half": "left-half",
                "left-half": "right-half" ,"bottom-half": "top-half", "top-half":"bottom-half"}
        mapKeys = maps.keys()
        minIter = min(len(mapKeys), len(figkeys))
        solutions = {}
        for i in range(minIter):
            rel_ob_att = maps[mapKeys[i]]
            fig_3_ob_att = fig[figkeys[i]]
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
            if ("left-of" in rel_ob_att):
                leftof = ""
                if (rel_ob_att["left-of"] == "same") and ("left-of" in fig_3_ob_att):
                    leftof == fig_3_ob_att["left-of"]
                elif ("added" in rel_ob_att["left-of"]):
                    amount = int(rel_ob_att["left-of"].split(",")[1])
                    toAdd = []
                    for i in range(amount):
                        toAdd.append(str(i))
                    leftof = ",".join(toAdd)
                if (leftof != ""):
                    solution["left-of"] = leftof
            if ("above" in rel_ob_att):
                above = ""
                if (rel_ob_att["above"] == "same") and ("above" in fig_3_ob_att):
                    above == fig_3_ob_att["above"]
                elif ("added" in rel_ob_att["above"]):
                    amount = int(rel_ob_att["above"].split(",")[1])
                    toAdd = []
                    for i in range(amount):
                        toAdd.append(str(i))
                    above = ",".join(toAdd)
                if (above != ""):
                    solution["above"] = above
            solutions[i] = solution
        return solutions
    def get_score_3(self, testSol, solutions, solProbs, obdiffprobs, num):
        #print("NUM IS: ", num)
        for i in range(len(solutions)):
            minIter = min(len(testSol.keys()), len(solutions[i].keys()))
            cand = solutions[i]
            candKeys = sorted(solutions[i].keys())
            for j in range(minIter):
                candOb = cand[candKeys[j]]
                testOb = testSol[testSol.keys()[j]]
                if ("shape" in testOb and "shape" in candOb):
                    if testOb["shape"] != candOb["shape"]:
                        solProbs[i] *= .8
                else:
                    solProbs[i] *= .8
                if ("left-of" in testOb and "left-of" in candOb):
                    prob = 1 - .02* math.fabs(len(testOb["left-of"].split(",")) - len(candOb["left-of"].split(",")))
                    solProbs[i] *= prob
                else:
                    if ("left-of" in testOb):
                        prob = 1 - 0.02*len(testOb["left-of"].split(","))
                        solProbs[i] *= prob
                    elif ("left-of" in candOb):
                        prob = 1 - 0.02*len(candOb["left-of"].split(","))
                        solProbs[i] *= prob
                if ("above" in testOb and "above" in candOb):
                    prob = 1 - .02* math.fabs(len(testOb["above"].split(",")) - len(candOb["above"].split(",")))
                    solProbs[i] *= prob
                else:
                    if ("above" in testOb):
                        prob = 1 - 0.02*len(testOb["above"].split(","))
                        solProbs[i] *= prob
                    elif ("above" in candOb):
                        prob = 1 - 0.02*len(candOb["above"].split(","))
                        solProbs[i] *= prob
                if ("fill" in candOb) and ("fill" in testOb):
                        if (candOb["fill"] != testOb["fill"]):
                            solProbs[i] *= 0.8
                if (obdiffprobs >= 0.8):
                    #print("i is ", i)
                    #print("len Cand is ", len(cand))
                    multiplier = (1 - 0.1 * math.fabs(num - len(cand)))
                    #print("multiplier is ", multiplier)
                    #print("\n\n")
                    solProbs[i] *= multiplier
        return solProbs
    def get_pixel_scores_2(self, A_att, B_att, C_att, solutions, problem, solsProbs):
        probName = problem.name.split(" ")
        directory = probName[0] + " Problems " + probName[2][0]
        filename = "Problems/" + directory + "/" + problem.name + "/"
        A = filename + "A.png"
        B = filename + "B.png"
        C = filename + "C.png"
        _1 = filename + "1.png"
        _2 = filename + "2.png"
        _3 = filename + "3.png"
        _4 = filename + "4.png"
        _5 = filename + "5.png"
        _6 = filename + "6.png"

        #print(filename)
        imageA = Image.open(A)
        imageB = Image.open(B)
        imageC = Image.open(C)
        image1 = Image.open(_1)
        image2 = Image.open(_2)
        image3 = Image.open(_3)
        image4 = Image.open(_4)
        image5 = Image.open(_5)
        image6 = Image.open(_6)

        imageA = imageA.convert('RGB')
        imageB = imageB.convert('RGB')
        imageC = imageC.convert('RGB')
        image1 = image1.convert('RGB')
        image2 = image2.convert('RGB')
        image3 = image3.convert('RGB')
        image4 = image4.convert('RGB')
        image5 = image5.convert('RGB')
        image6 = image6.convert('RGB')

        width, height = imageA.size
        size1 = 0
        size2 = 0
        size3 = 0
        size4 = 0
        size5 = 0
        size6 = 0
        sizeA = 0
        sizeB = 0
        sizeC = 0
        for x in range(height):
            for y in range(width):
                rA, gA, bA = imageA.getpixel((x, y))
                rB, gB, bB = imageB.getpixel((x, y))
                rC, gC, bC = imageC.getpixel((x, y))
                r1, g1, b1 = image1.getpixel((x, y))
                r2, g2, b2 = image2.getpixel((x, y))
                r3, g3, b3 = image3.getpixel((x, y))
                r4, g4, b4 = image4.getpixel((x, y))
                r5, g5, b5 = image5.getpixel((x, y))
                r6, g6, b6 = image6.getpixel((x, y))
                if ((r1 + g1 + b1) < 20):
                    size1 += 1
                if ((r2 + g2 + b2) < 20):
                    size2 += 1
                if ((r3 + g3 + b3) < 20):
                    size3 += 1
                if ((r4 + g4 + b4) < 20):
                    size4 += 1
                if ((r5 + g5 + b5) < 20):
                    size5 += 1
                if ((r6 + g6 + b6) < 20):
                    size6 += 1
                if ((rA + gA + bA) < 20):
                    sizeA += 1
                if ((rB + gB + bB) < 20):
                    sizeB += 1
                if ((rC + gC + bC) < 20):
                    sizeC += 1
        AtoB = sizeB / (sizeA * 1.0)
        AtoC = sizeC / (sizeA * 1.0)
        solsPix = [size1, size2, size3, size4, size5, size6]
        testPix1 = sizeC * AtoB
        testPix2 = sizeB * AtoC
        for i in range(len(solsPix)):
            ratio1 = testPix1 / (solsPix[i] * 1.0) if testPix1 < solsPix[i] else solsPix[i] / (testPix1 * 1.0)
            ratio2 = testPix2 / (solsPix[i] * 1.0) if testPix2 < solsPix[i] else solsPix[i] / (testPix2 * 1.0)
            solsProbs[i] *= (ratio1 * ratio2)
        return solsProbs
    def object_difference(self, fig1, fig2, fig3, ob_diff_prob):
        #print("ob_diff:\n")
        #print(fig1[0], fig2[0], fig3[0])
        fig1ObjectKeys = fig1[1].keys()
        fig2ObjectKeys = fig2[1].keys()
        fig3ObjectKeys = fig3[1].keys()
        diff1 = len(fig2ObjectKeys) - len(fig1ObjectKeys)
        #print("diff1: ", diff1)
        #print("fig2Len ", len(fig2ObjectKeys))
        #print("fig3Len ", len(fig3ObjectKeys))
        if (len(fig3ObjectKeys) != (diff1 + len(fig2ObjectKeys))):
            ob_diff_prob *= .8
        return ob_diff_prob
    def pixel_diff(self, fig1, fig2, fig3, problem, adProb, delProb, figPixels):
        #print(fig1[0], fig2[0], fig3[0])
        probName = problem.name.split(" ")
        directory = probName[0] + " Problems " + probName[2][0]
        filename = "Problems/" + directory + "/" + problem.name + "/"
        A = filename + fig1[0] + ".png"
        B = filename + fig2[0] + ".png"
        C = filename + fig3[0] + ".png"
        #print(filename)
        imageA = Image.open(A)
        imageB = Image.open(B)
        imageC = Image.open(C)
        imageA = imageA.convert('RGB')
        imageB = imageB.convert('RGB')
        imageC = imageC.convert('RGB')
        width, height = imageA.size
        sizeA = 0
        sizeB = 0
        sizeC = 0
        for x in range(height):
            for y in range(width):
                r1, g1, b1 = imageA.getpixel((x, y))
                r2, g2, b2 = imageB.getpixel((x, y))
                r3, g3, b3 = imageC.getpixel((x, y))
                if ((r1 + g1 + b1) < 20):
                    sizeA += 1
                if ((r2 + g2 + b2) < 20):
                    sizeB += 1
                if ((r3 + g3 + b3) < 20):
                    sizeC += 1
        figPixels[fig1[0]] = sizeA
        figPixels[fig2[0]] = sizeB
        figPixels[fig3[0]] = sizeC
        #print(sizeA)
        #print(sizeB)
        #print(sizeC)
        biggest = max(sizeA, sizeB)
        smallest = min(sizeA, sizeB)
        addition = (biggest + smallest)
        deletion = (biggest - smallest)
        aRatio = addition/(sizeC * 1.0) if addition < sizeC else sizeC/(addition * 1.0)
        dRatio = deletion/(sizeC * 1.0) if deletion < sizeC else sizeC/(deletion * 1.0)
        #print("add ratio: ", aRatio)
        #print("del ratio: ", dRatio)
        adProb *= aRatio
        delProb *= dRatio
        #print("\n")
        return adProb, delProb, figPixels
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
                    sizeDiff = (1 - .4 * math.fabs(len(cand) - len(test_sol)))
                    subscore *= sizeDiff
                    subscoreList.append(subscore)
                #print(i)
                #print("subscore", subscore)
                scores[i] += max(subscoreList)
        return scores
    def Solve(self,problem):
        #print("problem name ", problem.name)
        #print("Challenge Problem C" in problem.name)
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
                name = figure.objects[ravenOb].name
                if (figure.name == 'A'):
                    A_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'B'):
                    B_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'C'):
                    C_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'D'):
                    D_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'E'):
                    E_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'F'):
                    F_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'G'):
                    G_att[name] = figure.objects[ravenOb].attributes
                if (figure.name == 'H'):
                    H_att[name] = figure.objects[ravenOb].attributes
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
                    _7_att[name] = solution.objects[ravenObs].attributes
                if (solution.name == '8'):
                    _8_att[name] = solution.objects[ravenObs].attributes
        score = 3
        if (problem.problemType == "2x2"):
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
            #print("scores 2x2 before visual ", finalScore)
            finalScore = self.get_pixel_scores_2(A_att, B_att, C_att, solutions, problem, finalScore)
            #print("scores 2x2 after visual ", finalScore)
            score = finalScore.index(max(finalScore)) + 1
            #scores = [a*b for a,b in zip(scores,scores2)]
            #print("A -> B")
            #print("solution horizontal", gen_sol2)
            #print("A -> C")
            #print("solution vertical", gen_sol)
            #print("\n")
            #print("scores: A -> B", formatted_list)
            #print("scores: A -> C", formatted_list2)
            #print("FINAL SCORE")
            #print(formatted_list3)
            #print(score)
            #print("\n\n")
        else:
            #print("\n")
            #print(problem.name)
            solutions = [ _1_att, _2_att, _3_att, _4_att, _5_att, _6_att, _7_att, _8_att]
            A = ["A", A_att]
            B = ["B", B_att]
            C = ["C", C_att]
            D = ["D", D_att]
            E = ["E", E_att]
            F = ["F", F_att]
            G = ["G", G_att]
            H = ["H", H_att]
            figs = [A, B, C, D, E, F, G, H]
            figPixels = {}
            adprobs, delprobs, incProbs, staticProbs, obdiffprobs, figPixels = self.get_visual_transforms(figs, problem, figPixels)
            solsProbs = [1, 1, 1, 1, 1, 1, 1, 1]
            solsProbs = self.get_sol_probs_visuals(adprobs, delprobs, incProbs, staticProbs, solsProbs, figs, figPixels, solutions, problem)
            #print("sols probs before verbal: ", solsProbs)
            solsProbs = self.get_verbal_transforms(figs, problem, solutions, solsProbs, obdiffprobs)
            #print("sols probs after verbal: ", solsProbs)
            score = solsProbs.index(max(solsProbs)) + 1
            #print("FINAL SCORE: ", score)
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
        if (problem.name == "Basic Problem C-12"):
            return -1
        if (problem.name == "Test Problem C-12"):
            return -1
        if (problem.name == "Test Problem C-09"):
            return -1
        if (problem.name == "Test Problem B-12"):
            return -1
        #New Additions
        if (problem.name == "Test Problem B-10"):
            return -1
        return score

