--
-- Created by IntelliJ IDEA.
-- User: momo
-- Date: 18-6-26
-- Time: 下午2:18
-- To change this template use File | Settings | File Templates.
--

cmd = torch.CmdLine()
cmd:option('-input','','input torch file')

local params = cmd:parse(arg)
local input_file = params.input

local t = torch.load(input_file)
--print(t.labels)
t.labels = t.labels:mul(-1):add(1)
--print(t.labels)
torch.save(input_file,t)
