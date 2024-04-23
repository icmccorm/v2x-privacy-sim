eval-dp:
	@./scripts/eval/run_all_dp_in_parallel.sh
eval:
	@./scripts/eval/run_all.sh
test:
	@python3 ./scripts/tracker.py -fq 1 -pc 1 -sb 0.00001 --debug --dir data
