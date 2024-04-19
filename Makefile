eval-dp:
	@./scripts/eval/run_all_dp_in_parallel.sh
eval:
	@./scripts/eval/run_all.sh
test:
	@python3 ./scripts/tracker.py -q -fq 1 -pc 1 -pb 0.01 -hb 0.01 -sb 0.01 --debug --dir data
