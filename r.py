import os, sys, re, csv
from pprint import pprint

def read_upsid(f = 'UPSID_MATRIX.txt'):
	upsid = {}
	phoneme_indices = {}
	with open(f) as rf:
		reader = csv.reader(rf, delimiter = '\t',  quotechar=None)
		for i, line in enumerate(reader):
			language = line[0].lower()
			phonemes = {}
			for j, p in enumerate(line[1:]):
				if len(p) > 0:
					phonemes[j] = p
					if j not in phoneme_indices:
						phoneme_indices[j] = p
			upsid[language] = phonemes
	return upsid, phoneme_indices

def read_upsid_desc(f = 'upsid_descs.txt'):
	descs = {}
	with open(f) as rf:
		reader = csv.reader(rf, delimiter = '\t', quotechar = None)
		# columns names
		next(reader)
		for i, (p, d) in enumerate(reader):
			descs[p] = d
	#		if i > 100:	break
	return descs

def read_wals(f = 'language.csv'):
	wals = {}
	feature_indices = {}
	with open(f) as rf:
		reader = csv.reader(rf, delimiter = ',',  quotechar=None)
		
		col_labels = next(reader)
		for i, label in enumerate(col_labels):
			feature_indices[i] = label

		for i, line in enumerate(reader):
			f_dict = {}
				
			for j, feature in enumerate(line):
				if j == 3:
					language = feature.lower()
				elif len(feature) > 0:
					f_dict[j] = feature
			wals[language] = f_dict

	return wals, feature_indices



class Lang(object):
	def __init__(self, name, phonemes, wals_features):
		self.name = name
		self.phonemes = phonemes
		self.features = wals_features

def aggregate_upsid_wals(upsid, wals):
	d = {}
	ulangs = set(upsid.keys())
	wlangs = set(wals.keys())
	for i, upsid_l in enumerate(sorted(ulangs)):
		if upsid_l not in wlangs:
			for j, wals_l in enumerate(wlangs):
				if re.search(upsid_l, wals_l):
					d[upsid_l] = Lang(upsid_l, upsid[upsid_l], wals[wals_l])
					break
		else:
			d[upsid_l] = Lang(upsid_l, upsid[upsid_l], wals[upsid_l])
	return d



def sparse_dict_to_list(d, sparse_size, binary = False):
	l = []
	for i in range(sparse_size):
		if binary:
			if i in d:
				l.append('1')
			else:
				l.append('0')
		else:
			if i in d:
				l.append(d[i])
			else:
				l.append('')
	return l

def main():
	upsid, phoneme_indices = read_upsid()
	wals, feature_indices = read_wals()
	phones_and_descs = read_upsid_desc()

	d = aggregate_upsid_wals(upsid, wals)

	total_phonemes = len(phoneme_indices)
	total_walsfeatures = len(feature_indices)
	with open('upsid.R_ready.txt', 'w') as wf:
		
		phones_as_list = sparse_dict_to_list(phoneme_indices, total_phonemes)
		phones_as_list = [phones_and_descs[p] for p in phones_as_list]
		wf.write('\t'.join(['name'] + phones_as_list))
		wf.write('\n')

		for l, l_data in sorted(d.items(), key = lambda x : x[0]):
			phones_as_list = sparse_dict_to_list(l_data.phonemes, total_phonemes, binary = True)
			wf.write('\t'.join([l] + phones_as_list))
			wf.write('\n')	
		
	with open('wals.R_ready.txt', 'w') as wf:

		wals_as_list = sparse_dict_to_list(feature_indices, total_walsfeatures)
		wf.write('\t'.join(['name'] + wals_as_list))
		wf.write('\n')
		
		for l, l_data in sorted(d.items(), key = lambda x : x[0]):
			wals_as_list = sparse_dict_to_list(l_data.features, total_walsfeatures)
			wf.write('\t'.join([l] + wals_as_list))
			wf.write('\n')
		

if __name__ == '__main__':
	main()
		
