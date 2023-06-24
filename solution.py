import os, glob ,re,sys
import imaging_interview
import cv2
from datetime import datetime
from PIL import Image
import logging
import argparse
import shutil, json, tqdm
#Logging setup 
logging.basicConfig(filename='ImagePreprocessorlog.txt',
                    filemode='w',
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt='%m/%d/%Y %I:%M:%S %p',level='DEBUG')
logging.getLogger('PIL').setLevel(logging.WARNING)
logger = logging.getLogger('ImagePreprocessor')


def process_dataset(root,outpath):
    pathlist = glob.glob(os.path.join(root,'*'))
    logger.debug('Copying files')
    for p in pathlist:
        oldfilename = os.path.abspath(p)

        # check for broken files and ingore them
        try:
            img=Image.open(oldfilename)
            img.verify()
        except(IOError,SyntaxError)as e:
            logger.info('Bad file  :  '+oldfilename)
            continue
        # Check for unixtime stamps and rename them to datetime format 
        headtail = os.path.split(oldfilename)
        searchstr = re.split('-',headtail[1])
        if len(searchstr) ==1:
            shutil.copy(oldfilename,os.path.join(outpath,headtail[1]))
            continue
        
        namesplit = searchstr[1].split('.')
        timest = float(namesplit[0])/1000
        timestmp = datetime.utcfromtimestamp(timest).strftime('%Y_%m_%d_%H_%M_%S')
        newfilename = os.path.join(outpath,searchstr[0]+'_'+timestmp+'.'+namesplit[1])
        shutil.copy(oldfilename,newfilename)
        # logger.debug('Copied file {0} to {1}'.format(oldfilename,newfilename))

def find_duplicates(path_list,Kernel_size=5,min_contour_area=100,duplicate_threshold=1000) :
    filter_list = []
    for i in tqdm.tqdm(range(len(path_list)-1)):
        currentframe = path_list[i]
        nextframe = path_list[i+1]
        img1 = cv2.imread(currentframe)
        img2 = cv2.imread(nextframe)
        logger.debug('Comparing image {0} with {1}'.format(currentframe,nextframe))
        # resize images to same size for comparison
        if img2.shape != img1.shape:
            logger.info('Resizing images')
            (h,w,_) = min(img1.shape,img2.shape)
            img1 = cv2.resize(img1,(w,h),interpolation=cv2.INTER_AREA)
            img2 = cv2.resize(img2,(w,h),interpolation=cv2.INTER_AREA)
        # image preprocess and compute similarity
        img_gray1 = imaging_interview.preprocess_image_change_detection(img1,[Kernel_size])
        img_gray2 = imaging_interview.preprocess_image_change_detection(img2,[Kernel_size])
        score, _, _ = imaging_interview.compare_frames_change_detection(img_gray1,img_gray2,min_contour_area)
        dup = score < duplicate_threshold
        result = {'currentframe':currentframe,'nextframe':nextframe,'sim_score':score,'duplicate':dup}
        filter_list.append(result)
    return filter_list

def remove_duplicates(filter_list):
    for item in filter_list:
        if item['duplicate']:
            logger.info('Duplicate image: {0}'.format(item['nextframe']))
            os.remove(item['nextframe'])
            logger.info('Removed!!')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Image preprocessor',description='Dataset preprocessor')
    parser.add_argument('-root','-r', type=str,default=r'./dataset-candidates-ml/dataset',help='Dataset root path directory')
    parser.add_argument('-gkernelsize','-k', type=int,default=21,help='Gaussian blur kernel size')
    parser.add_argument('-minCntArea','-mc', type=int,default=100,help='Minimum Contours area')
    parser.add_argument('-dupthreshold','-st', type=int,default=1000,help='Image duplication threshold')
    args = parser.parse_args()

    logger.info('Starting Preprocessing..')
    root = os.path.abspath(args.root)
    outpath = os.path.join(root,'../dataset_filtered')
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    else:
        logger.error('Output path already exists!! clean and restart..')
        sys.exit(-1)
    logger.debug('Root path {0}'.format(args.root))
    logger.debug('Output path {0}'.format(outpath))
    logger.debug('Args kernel size: {0}, Min Contour Area: {1}, Simiarlity threshold: {2}'.format(args.gkernelsize,args.minCntArea,args.dupthreshold))
    #Clean folder names and files
    process_dataset(root,outpath)
    datasetlist = sorted(glob.glob(os.path.join(outpath,'*')))
    #Find similar images
    filter_list = find_duplicates(datasetlist,args.gkernelsize,args.minCntArea,args.dupthreshold)
    #save results
    with open('dataset_filter_results.json','w') as f:
        json.dump({'result':filter_list},f,indent=6)
    #remove duplicates
    remove_duplicates(filter_list)
    logger.info('Processing complete!!')




