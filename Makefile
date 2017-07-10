simple:
	#./analyse_bipartite_matches_new.py --width 839 --height 396 Skeletons-2/TXT/Matches-symmetric/*.txt
	./make_persistence_diagrams.py --width 839 --height 396 Skeletons-2/TXT/Matches-symmetric-pixel-ages-new/Ages_t??.txt


21_14:
	#./process_matches.py 21_14/Matches/Matches_*.txt
	#./analyse_bipartite_matches_new.py --width 1304 --height 722 21_14/Matches/*.txt > Ages_21_14.txt
	./make_persistence_diagrams.py --width 1304 --height 722 --prefix=21_14_ --path 21_14 21_14/Ages/Ages_t??.txt


simulation:
	#./process_matches.py Simulation/Matches/Matches_*.txt
	#./analyse_bipartite_matches_new.py --width 1500 --height 1000 Simulation/Matches/*.txt > Ages_simulation.txt
	./make_persistence_diagrams.py --width 1000 --height 1500 --prefix=Simulation_ --path Simulation Simulation/Ages/Ages_t??.txt

vivacity:
	./vivacity_per_segment.py Skeletons-2/TXT/Matches-symmetric-growth-persistence-new/t??_growth_persistence.txt > /tmp/Vivacity_example.txt
	./vivacity_per_segment.py --width 1304 --height 722 --prefix=21_14_ --path 21_14 21_14/Growth-persistence/t??_growth_persistence.txt > /tmp/Vivacity_21_14.txt
	./vivacity_per_segment.py --width 1000 --height 1500 --prefix=Simulation_ --path Simulation Simulation/Growth-persistence/t??_growth_persistence.txt > /tmp/Vivacity_simulation.txt
