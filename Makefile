eval-dp:
	@./scripts/eval/run_all_dp.sh
eval:
	@./scripts/eval/run_all_dp.sh
test:
	@python3 ./scripts/tracker.py -fq 1 -pc 1 -pb 0.1 --debug --dir data