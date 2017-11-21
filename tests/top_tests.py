import unittest
import sys

sys.path.append('../')
sys.path.append('../plugins')
import top

class TestTopModule(unittest.TestCase):

    def test_parse_player_data(self):
        raw_data = [
            '# 1 \U0001f1fb\U0001f1e6Анунах 66/2107194',
            '# 2 \U0001f1f0\U0001f1eeKeeke 66/2082585', 
            '# 3 \U0001f1ea\U0001f1faЗмея 66/2059968',  
            '# 4 \U0001f1fb\U0001f1e6su4ara 9KA 65/2000135',  
            '# 5 \U0001f1f0\U0001f1eeAaarrggh 1OП 65/2000000',  
            '# 6 \U0001f1fb\U0001f1e6Ливает из чв 65/1991502',  
            '# 7 \U0001f1ec\U0001f1f5SoldierKh 65/1988284',  
            '# 8 \U0001f1fb\U0001f1e6за Мятку и YLT 65/1976977',  
            '# 9 \U0001f1fb\U0001f1e6\U0001f990Drama King 65/1976349',
            '# 10 \U0001f1ea\U0001f1faЗмееlove 65/1935584',
            '# 310 \U0001f1e8\U0001f1feзабор 59/1124832',
            '# 311 \U0001f1ee\U0001f1f2asasay RUBY 59/1124663',
            '# 312 \U0001f1e8\U0001f1fekapkacДекаданс 59/1121446'
        ]
        expected_data = [
            { 'name' : 'Анунах', 'position': '1', 'flag' : 'yellow', 'level' : '66', 'xp' : '2107194' },
            { 'name' : 'Keeke', 'position': '2', 'flag' : 'twilight', 'level' : '66', 'xp' : '2082585' },
            { 'name' : 'Змея', 'position': '3', 'flag' : 'blue', 'level' : '66', 'xp' : '2059968' },
            { 'name' : 'su4ara 9KA', 'position': '4', 'flag' : 'yellow', 'level' : '65', 'xp' : '2000135' },
            { 'name' : 'Aaarrggh 1OП', 'position': '5', 'flag' : 'twilight', 'level' : '65', 'xp' : '2000000' },   
            { 'name' : 'Ливает из чв', 'position': '6', 'flag' : 'yellow', 'level' : '65', 'xp' : '1991502' },
            { 'name' : 'SoldierKh', 'position': '7', 'flag' : 'black', 'level' : '65', 'xp' : '1988284' },   
            { 'name' : 'за Мятку и YLT', 'position': '8', 'flag' : 'yellow', 'level' : '65', 'xp' : '1976977' },  
            { 'name' : '\U0001f990Drama King', 'position': '9', 'flag' : 'yellow', 'level' : '65', 'xp' : '1976349' },   
            { 'name' : 'Змееlove', 'position': '10', 'flag' : 'blue', 'level' : '65', 'xp' : '1935584' },
            { 'name' : 'забор', 'position': '310', 'flag' : 'white', 'level' : '59', 'xp' : '1124832' },   
            { 'name' : 'asasay RUBY', 'position': '311', 'flag' : 'red', 'level' : '59', 'xp' : '1124663' },   
            { 'name' : 'kapkacДекаданс', 'position': '312', 'flag' : 'white', 'level' : '59', 'xp' : '1121446' }
        ]        
        index = 0
        for item in raw_data:            
            player = top.parse_player_data(item)
            self.assertEqual(player['name'], expected_data[index]['name'])
            self.assertEqual(player['position'], expected_data[index]['position'])
            self.assertEqual(player['flag'], expected_data[index]['flag'])
            self.assertEqual(player['level'], expected_data[index]['level'])
            self.assertEqual(player['xp'], expected_data[index]['xp'])
            index += 1       

if __name__ == '__main__':
    unittest.main()