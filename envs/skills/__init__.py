
from gym.envs.mujoco.mujoco_env import MujocoEnv
# ^^^^^ so that user gets the correct error
# message if mujoco is not installed correctly

# Base class
from gym.envs.skills.base_env import BaseEnv

# Walker2d
from gym.envs.skills.walker2d import Walker2dEnv
from gym.envs.skills.walker2d_forward import Walker2dForwardEnv
from gym.envs.skills.walker2d_backward import Walker2dBackwardEnv
from gym.envs.skills.walker2d_balance import Walker2dBalanceEnv
from gym.envs.skills.walker2d_jump import Walker2dJumpEnv
from gym.envs.skills.walker2d_crawl import Walker2dCrawlEnv
from gym.envs.skills.walker2d_patrol import Walker2dPatrolEnv
from gym.envs.skills.walker2d_hurdle import Walker2dHurdleEnv
from gym.envs.skills.walker2d_obstacle_course import Walker2dObstacleCourseEnv

from gym.envs.skills.walker2d_forward_vel_1 import Walker2dForwardEnv_vel_1
from gym.envs.skills.walker2d_forward_vel_2 import Walker2dForwardEnv_vel_2
from gym.envs.skills.walker2d_forward_vel_3 import Walker2dForwardEnv_vel_3
from gym.envs.skills.walker2d_forward_vel_4 import Walker2dForwardEnv_vel_4
from gym.envs.skills.walker2d_forward_vel_5 import Walker2dForwardEnv_vel_5
from gym.envs.skills.walker2d_forward_vel_6 import Walker2dForwardEnv_vel_6

from gym.envs.skills.walker2d_backward_vel_1 import Walker2dBackwardEnv_vel_1
from gym.envs.skills.walker2d_backward_vel_2 import Walker2dBackwardEnv_vel_2
from gym.envs.skills.walker2d_backward_vel_3 import Walker2dBackwardEnv_vel_3
from gym.envs.skills.walker2d_backward_vel_4 import Walker2dBackwardEnv_vel_4
from gym.envs.skills.walker2d_backward_vel_5 import Walker2dBackwardEnv_vel_5
from gym.envs.skills.walker2d_backward_vel_6 import Walker2dBackwardEnv_vel_6

from gym.envs.skills.walker2d_highkneerun_v1 import Walker2dHighKneeRun1Env
from gym.envs.skills.walker2d_highkneerun_v2 import Walker2dHighKneeRun2Env

from gym.envs.skills.walker2d_frogjump import Walker2dFrogJumpEnv
from gym.envs.skills.walker2d_frogjump_forward import Walker2dFrogJumpForwardEnv

from gym.envs.skills.walker2d_crawl_2 import Walker2dCrawl2Env

from gym.envs.skills.walker2d_jump_2 import Walker2dJump2Env