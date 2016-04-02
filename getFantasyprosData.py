import csv
import time
import json
import requests
import random

pos_list = ['QB', 'WR', 'RB', 'TE', 'DST', 'K']
output_data = []
header_row = ['Player', 'PlayerID', 'PlayerPosition', 'PlayerTeam', 'ProjectedPTS', 'PTSRanking', 'FDSalary', 'FDSalaryRank', 'Week', 'Season']
output_data.append(header_row)
expert_id = '532'
week = 1


def getRazzed():
	while week < 18:
		global week
		print 'On Week {0} of 17'.format(week)
		for pos in pos_list:
			time.sleep(random.random() * .25 + .25)
			print '     on {0}'.format(pos)
			url = 'https://partners.fantasypros.com/api/v1/expert-dfs-projections.php?sport=NFL&year=2015&week={0}&id={1}&position={2}&type=DFS&site=FD&export=csv'.format(week, expert_id, pos)
			raw_source = requests.get(url)
			raw_text = raw_source.content
			json_dict = json.loads(raw_text) 
			for player in json_dict['players']:
				global output_data
				player_row = []
				player_row.extend((str(player['player_name']), player['player_id'], pos, str(player['team']), player['pts'], player['pts_rank'], player['salary'], player['salary_rank'], str(json_dict['week']), str(json_dict['year'])))
				output_data.append(player_row)	
		week += 1
		time.sleep(random.random() * 2 + 1)

def ListToCSV(): ## writes the tablerows array to a CSV file. This function is just a slightly altered version of a popular script from stackoverflow
	filepath = '/Users/robertgreer/Dropbox/Python Codes/DFSpull/'
	filename = 'RAZZ{0}DFSdata.csv'.format(str(time.strftime("%Y%m%d")))
	with open(filepath + filename, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(output_data)

def main():
	getRazzed()
	ListToCSV()

if __name__ == '__main__':
	main()
