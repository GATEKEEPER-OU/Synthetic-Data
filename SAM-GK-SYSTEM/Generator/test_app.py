import argparse
from dataGenModel import DataGenModel

# Codings user can start with
coding = ['41950-7', '85354-9', '8867-4', '9108-2', '93829-0', '93830-8', '93831-6', '93832-4', 'floor-climbed','LP412113-5', 'LA11834-1']

def main():
    # create parser
    parser = argparse.ArgumentParser()
    
    # add arguments to the parser
    parser.add_argument("code")
    parser.add_argument("numEvents", type=int)
    parser.add_argument("temperature", type=float)

    # parse the arguments
    args = parser.parse_args()
    code = args.code
    if code in coding:
        maxTimings = max(1, args.numEvents)
        eventTemperature = min(args.temperature, 1.0)
        
        data_generator = DataGenModel(code, maxTimings=maxTimings, eventTemperature = eventTemperature)
        results_file = data_generator.generate_single_user()
        print(results_file + ' has been generated and is awaitng evaluation')
    else:
        print('Code does not exsit')

if __name__ == '__main__':
    main()
