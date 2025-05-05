"""
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
"""

list_1 = [2,4,3]
list_2 =  [5,6,4]

# def Add_lst(lst_1, lst_2):
#     output = []

#     for i in range(len(list_1)):
#         for j in range(len(list_2)):
#             k = list_1[i] + list_2[j]
#             if k < 9:
#                 output.append(k)
#             else:
#                 output.append(0)
#             break

#     return output

# print(Add_lst(list_1, list_2))

# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        output = []
        l1.reverse()
        l2.reverse()
        #print(l1)
        #print(l2)
        
        for i in range(len(l1)):
            for j in range(len(l2)):
                k = l1[i] + l2[j] 
                if k < 9:
                    output.append(k)

                else:
                    output.append(0)
            break
        return output 
d = Solution()

ls1 = [9,9,9,9,9,9,9]
ls2 = [9,9,9,9]
print(d.addTwoNumbers(ls1,ls2))

#print(d.addTwoNumbers(list_1,list_2))