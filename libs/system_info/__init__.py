# -*- encoding: utf-8 -*-
import sys

if sys.platform.startswith('win'):
    from system_info.win import get_cpu_style, get_cpu_usage, get_mem_usage, get_ip,get_process_info
else:
    from system_info.linux import get_cpu_style, get_cpu_usage, get_mem_usage, get_ip,get_process_info
