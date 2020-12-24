def main(argv):
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--input-dir", required=True)
    argparser.add_argument("-o", "--output-dir", required=True)
    argparser.add_argument("-d", "--done-dir", required=True)
    argparser.add_argument("-t", "--targeted-duration-in-seconds", default=600, type=int)
    args = argparser.parse_args(argv[1:])
    import os
    input_files = os.listdir(args.input_dir)
    input_files.sort()
    import moviepy.editor as mvpye
    current_clip_batch = []
    current_clip_batch_duration = 0
    current_clip_batch_names = []
    for f in input_files:
        clip = mvpye.VideoFileClip(args.input_dir + "/" + f) 
        if (current_clip_batch_duration + clip.duration) > args.targeted_duration_in_seconds:
            target_name = args.output_dir + '/from-' + \
                    current_clip_batch_names[0] + '-till-' + \
                    current_clip_batch_names[-1:][0]
            mvpye.concatenate_videoclips(current_clip_batch). \
                write_videofile(target_name)
            for c in current_clip_batch_names:
                os.rename(args.input_dir + '/' + c, args.done_dir + '/' + c) 
            current_clip_batch = []
            current_clip_batch_duration = 0
            current_clip_batch_names = []
        else:
           current_clip_batch_duration += clip.duration
           current_clip_batch.append(clip)
           current_clip_batch_names.append(f)
           print(f"Current clip {f}, duration {current_clip_batch_duration}.")
    

if __name__ == "__main__":
    import sys
    main(sys.argv)
