eval-dp:
	@./scripts/eval/run_all_dp_in_parallel.sh 0.8 0.004 0.3
eval:
	@./scripts/eval/run_all.sh
test:
	@python3 ./scripts/tracker.py -fq 1 -pc 1 -pb 0.1 -sb 0.1 -hb 0.1 --debug --dir data
