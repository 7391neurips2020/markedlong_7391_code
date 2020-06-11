#!/bin/bash
rand=$(pwgen 13 1) # leave only letters and numbers
echo "$rand"
expt_name="NAME_REMOVED_marklong_len$1_$rand"
echo "Experiment name: $expt_name"
#  baseline dataset, easiest setting of length and curvature

# curvature  -- difficulty_level
# 0.15      --   0
# 0.25      --   1
# 0.35      --   2

# length -- difficulty_level
# 10    --   0
# 13    --   1
# 16    --   2

# python contour_draw_PIL.py -sd ./ -wd 256 -r 0.15 -pr 30 -pl 12 -tc 255 -bc 255 -ns 100000 -en curv0len0_100k -c True

# increasing difficulty by increasing length of closed path and keeping curvature constant
python connected_contour_draw.py -sd ./ -wd 256 -pl $1 -ns $2 -en $expt_name -ml True -ds True
#python contour_draw_PIL.py -sd ./ -wd 256 -r 0.15 -pr 30 -pl 20 -tc 255 -bc 255 -ns 100000 -en curv0len2_100k -c True

# increasing difficulty by increasing curvature and keeping length constant
# python contour_draw_PIL.py -sd ./ -wd 256 -r 0.25 -pr 30 -pl 12 -tc 255 -bc 255 -ns 100000 -en curv1len0_100k -c True
# python contour_draw_PIL.py -sd ./ -wd 256 -r 0.35 -pr 30 -pl 12 -tc 255 -bc 255 -ns 100000 -en curv2len0_100k -c True
