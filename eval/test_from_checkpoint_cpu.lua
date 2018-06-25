--
-- Created by IntelliJ IDEA.
-- User: momo
-- Date: 18-6-22
-- Time: 上午10:16
-- To change this template use File | Settings | File Templates.
--

require 'torch'
require 'nn'
require 'optim'
require 'rnn'
require 'os'
--require 'cunn'
package.path = package.path ..';./model/batcher/?.lua'
package.path = package.path ..';../model/batcher/?.lua'
package.path = package.path ..';./model/module/?.lua'
package.path = package.path ..';../model/module/?.lua'
require 'MapReduce'
require 'BatcherFileList'
require 'SplitTableNoGrad'
require "ConcatTableNoGrad"
require "TopK"
require "LogSumExp"


cmd = torch.CmdLine()


cmd:option('-input_dir','','input dir which contains the list files for train/dev/test')
cmd:option('-out_file','','output dir for outputing score files')
cmd:option('-predicate_name','','output dir for outputing score files')
cmd:option('-meanModel',0,'to take the mean of scores of each path. Default is max (0)')
cmd:option('-model_path','','model name')

cmd:text()
local params = cmd:parse(arg)

local out_file = params.out_file
local input_dir = params.input_dir
local predicate_name = params.predicate_name
local model_path = params.model_path

assert(input_dir~='','input_dir isnt set. Point to the dir where train/dev/test.list files reside')


data_files={input_dir..'/'..predicate_name}
local shuffle = false
local maxBatches = 1000
local minibatch = 512
local useCuda = false
local testBatcher = BatcherFileList(data_files[1], minibatch, shuffle, maxBatches, useCuda, 'test.list')
--local labs,inputs,count,classId = testBatcher:getBatch()
--print(labs)
--print(inputs)
print("using model:", model_path)

local start_time = os.time()
local total_batch_count = 0
local check_file = io.open(model_path)
if check_file ~= nil then
    print("load model...")
    local predictor_net = torch.load(model_path).predictor_net
    local reducer = nn.Sequential():add(nn.LogSumExp(2)):add(nn.Squeeze(2))
    local training_net = nn.Sequential():add(nn.MapReduce(predictor_net,reducer)):add(nn.Sigmoid())
    local model = nn.Sequential():add(training_net):add(nn.Select(2,1))

    print('start predicting...')
--    local totalBatchCounter
    local batcher = testBatcher
--    totalBatchCounter = testBatchCounter
--    batcher:reset()

--    local out_file = out_dir_p..'/test.scores'
    local file = io.open(out_file, "w")

    local counter=0
    local batch_counter = 0
    while(true) do
        local labs,inputs,count,classId = batcher:getBatch()
        if(inputs == nil) then break end
        labs = labs
        inputs = inputs
        batch_counter = batch_counter + 1
        local preds = model:forward(inputs)
        for i=1,count do
            local score = preds[i]
            local socre_str = string.format("%.5f",score)
--            print(type(score))
--            print()
            local label = labs[i]
            file:write(counter..'\t'..socre_str..'\t'..label..'\n')
            counter = counter + 1
        end
        total_batch_count = total_batch_count+1
        if total_batch_count % 100 == 0 then
            print("batch nums:", total_batch_count, "per 100 batch cost time:", (os.time()-start_time)/(total_batch_count/100))
        end
        print("batch number:", total_batch_count)
    end
    file:close()
end

print("total cost time:", os.time()-start_time)