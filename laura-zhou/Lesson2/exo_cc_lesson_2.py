import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if not isinstance(n,int):
        return ("bad argument")
    if not isinstance(string,str):
        return ("bad argument")
    return n*string
 
# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
   if 9 in nums[:4]:
       return True
   else:
       return False
  

# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):  
    count=0
    for i in range(len(string)-2):
        if string[-2:]== (string[i]+string[i+1]):
            count+=1
    return count
   # return string[:-2].count(string[-2:])

#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
#map(lambda x: len(x), list)
def length_words(array):
    d=[]
    for i in array:
        d.append(len(i))
    return d

#write fizbuzz programm
 
def fizbuzz():
  for i in range(1,100):
      if (i%3==0 and i%5==0):
          print ("fizzbuzz")
      elif (i%3==0):
          print ("fizz")
      elif (i%5==0):
          print("buzz")
      else:
          print (i )      
  return 
 
#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    nombre=str(number)
    l=[]
    for i in nombre:
        l.append(int(i))
    return l
        


#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    l=text.split() 
    m=[]
    for i in l:
        m.append(i[1:].lower()+i[0].lower()+"ay") 
    p=' '.join(m)
    return p.capitalize()
    
# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")



def main():
    unittest.main()

if __name__ == '__main__':
    main()
