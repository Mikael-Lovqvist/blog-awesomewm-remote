import json, dbus
from pprint import pprint
from pathlib import Path

session_bus = dbus.SessionBus()
awful_service = session_bus.get_object('org.awesomewm.awful', '/')
awful_remote_if = dbus.Interface(awful_service, 'org.awesomewm.awful.Remote')
lua_eval = awful_remote_if.Eval

def screen_shot_all_windows():

	result = lua_eval(f'''

		local gears = require("gears");
		local res = {{}};

		for j, s in ipairs(screen) do
			for i, c in ipairs(s.all_clients) do

				-- local cres = gears.surface(c.content):write_to_png('/home/devilholk/Projects/awesomewm/remote-experiments/s' .. j .. '-c' .. i .. '.png');
				-- table.insert(res, {{j, i, cres}});
				table.insert(res, {{j, i, c.name}});
			end
		end

		return json.encode(res)

	''')

	try:
		return json.loads(result)
	except:
		raise RuntimeError(result)


def lua_eval_expect_json(code):

	result = lua_eval(code)

	try:
		return json.loads(result)
	except:
		raise RuntimeError(result)


def list_all_clients():
	return lua_eval_expect_json(f'''

		local res = {{}};
		for j, s in ipairs(screen) do
			for i, c in ipairs(s.all_clients) do
				table.insert(res, {{j, i, c.name}});
			end
		end

		return json.encode(res)

	''')


#Load json library if not loaded
if not bool(lua_eval('return json ~= nil')):
	lua_eval(Path('json_lib.lua').read_text())


for screen, client_id, client_name in list_all_clients():
	print(f'screen/client: {screen}/{client_id}		title: {client_name}')
