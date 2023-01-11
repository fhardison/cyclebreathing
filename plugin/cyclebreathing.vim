
if !has('python3')
	echomsg ':python3 not available'
	finish
endif

python3 import cyclebreathing.cycle
python3 cycler = cyclebreathing.cycle.Cycle()

command! AddBreathing python3 cycler.test()
