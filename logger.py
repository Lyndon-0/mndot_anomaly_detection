from loguru import logger
logger.remove()
logger.add(
	"logs/info_log.log",
	rotation="500 MB",
	level="INFO",
	# serialize=True,
	# enqueue=True,
	# backtrace=True,
	# diagnose=True,
	# catch=True,
	)