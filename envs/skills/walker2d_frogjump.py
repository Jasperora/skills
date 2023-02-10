import numpy as np

from gym import utils
from gym.envs.mujoco import mujoco_env

from gym.envs.skills.walker2d import Walker2dEnv

import wandb

class Walker2dFrogJumpEnv(Walker2dEnv):
    def __init__(self):
        super().__init__()

        # config
        self._config.update({
            "x_vel_reward": -1,
            "alive_reward": 1,
            "angle_reward": 0.1,
            "foot_reward": 0.01,
            "height_reward": 2,
            "x_vel_limit": 1,
            "min_height": 0.1,
            "foot_height_reward": 3,
            "jump_reward": 4,
            "height_diff_reward": 1,
            "thigh_foot_reward": 2,
            "foot_diff_reward": 2,
            "squat_reward": 4,
        })

        # state
        self.t = 0

        # see if agent jump
        self.jump = False

        # env info
        self.reward_type += ["x_vel_reward", "alive_reward", "angle_reward",
                             "foot_reward", "height_reward", "success", "foot_height_reward",
                             "jump_reward", "thigh_foot_reward", "height_diff_reward", "foot_diff_reward", "squat_reward",
                             "x_vel_mean", "height_mean", "nz_mean", "delta_h_mean"]
        self.ob_type = self.ob_shape.keys()

        mujoco_env.MujocoEnv.__init__(self, 'walker_v1.xml', 4)
        utils.EzPickle.__init__(self)

    def step(self, a):
        x_before = self.data.qpos[0]
        height_before = self.data.qpos[1]
        right_foot_before = self.data.qpos[5]
        left_foot_before = self.data.qpos[8]
        self.do_simulation(a, self.frame_skip)
        x_after = self.data.qpos[0]
        right_foot_after = self.data.qpos[5]
        left_foot_after = self.data.qpos[8]

        self._reset_external_force()
        if np.random.rand(1) < self._config["prob_apply_force"]:
            self._apply_external_force()

        done = False
        x_vel_reward = 0
        angle_reward = 0
        height_reward = 0
        alive_reward = 0
        ctrl_reward = self._ctrl_reward(a)

        height = self.data.qpos[1]
        angle = self.data.qpos[2]
        delta_h = self.data.body_xpos[1, 2] - max(self.data.body_xpos[4, 2], self.data.body_xpos[7, 2])
        nz = np.cos(angle)
        x_vel = (x_after - x_before) / self.dt
        # x_vel = self._config["x_vel_limit"] - abs(x_vel - self._config["x_vel_limit"])
        right_foot_vel = abs(right_foot_after - right_foot_before) / self.dt
        left_foot_vel = abs(left_foot_after - left_foot_before) / self.dt
        foot_height_diff = abs(self.data.body_xpos[4, 2] - self.data.body_xpos[7, 2])
        height_diff = abs(height - height_before)
        foot_diff = abs(self.data.body_xpos[4, 0] - self.data.body_xpos[7, 0]) + \
            abs(self.data.body_xpos[4, 1] - self.data.body_xpos[7, 1]) + \
            abs(self.data.body_xpos[4, 2] - self.data.body_xpos[7, 2])


        # reward
        x_vel_reward = self._config["x_vel_reward"] * abs(x_vel)
        angle_reward = self._config["angle_reward"] * nz
        height_reward = self._config["height_reward"] * min(self.data.body_xpos[4, 2], self.data.body_xpos[7, 2])
        alive_reward = self._config["alive_reward"]
        foot_reward = -self._config["foot_reward"] * (right_foot_vel + left_foot_vel)
        foot_height_reward = -self._config["foot_height_reward"] * foot_height_diff
        height_diff_reward = self._config["height_diff_reward"] * height_diff
        foot_diff_reward = -self._config["foot_diff_reward"] * foot_diff

        if height >= 1.5 and min(self.data.body_xpos[4, 2], self.data.body_xpos[7, 2]) > 0.3:
            jump_reward = self._config["jump_reward"]
        else:
            jump_reward = 0
        
        if height >= 1.5 and min(self.data.body_xpos[4, 2], self.data.body_xpos[7, 2]) > 0.3 or self.jump:
            self.jump = True
        else:
            self.jump = False

        if self.jump and self.data.body_xpos[1, 2] < 0.5:
            squat_reward = self._config["squat_reward"]
            self.jump = False
        else:
            squat_reward = 0
            
        if self.data.body_xpos[3, 2] > self.data.body_xpos[4, 2] and self.data.body_xpos[6, 2] > self.data.body_xpos[7, 2]:
            thigh_foot_reward = self._config["thigh_foot_reward"]
        else:
            thigh_foot_reward = 0

        reward = x_vel_reward + angle_reward + height_reward + jump_reward + \
            ctrl_reward + alive_reward + foot_reward + foot_height_reward + height_diff_reward + \
            thigh_foot_reward + foot_diff_reward + squat_reward

        # fail
        done = height < self._config["min_height"]
        self.t += 1
        success = not done and self.t >= 1000
        if success: done = True

        ob = self._get_obs()
        info = {"x_vel_reward": x_vel_reward,
                "ctrl_reward": ctrl_reward,
                "angle_reward": angle_reward,
                "height_reward": height_reward,
                "alive_reward": alive_reward,
                "foot_reward": foot_reward,
                "jump_reward": jump_reward,
                "height_diff_reward": height_diff_reward,
                "thigh_foot_reward": thigh_foot_reward,
                "foot_diff_reward": foot_diff_reward,
                "squat_reward": squat_reward,
                "delta_h_mean": delta_h,
                "nz_mean": nz,
                "x_vel_mean": (x_after - x_before) / self.dt,
                "height_mean": height,
                "success": success}
        wandb.log(info)
        return ob, reward, done, info

    def _get_obs(self):
        qpos = self.data.qpos
        qvel = self.data.qvel
        qacc = self.data.qacc
        return np.concatenate([qpos[1:], np.clip(qvel, -10, 10), qacc]).ravel()

    def get_ob_dict(self, ob):
        if len(ob.shape) > 1:
            return {'joint': ob[:, :17], 'acc': ob[:, 17:26]}
        else:
            return {'joint': ob[:17], 'acc': ob[17:26]}

    def reset_model(self):
        init_randomness = self._config["init_randomness"]
        qpos = self.init_qpos + np.random.uniform(low=-init_randomness,
                                                  high=init_randomness,
                                                  size=self.model.nq)
        qvel = self.init_qvel + np.random.uniform(low=-init_randomness,
                                                  high=init_randomness,
                                                  size=self.model.nv)
        self.set_state(qpos, qvel)

        # init target
        self._set_pos('target_forward', (10, 0, 0))
        self._set_pos('target_backward', (-10, 0, 0))

        # more perturb
        for _ in range(int(self._config["random_steps"])):
            self.do_simulation(self.unwrapped.action_space.sample(), self.frame_skip)
        self.t = 0

        return self._get_obs()

    def is_terminate(self, ob, init=False, env=None):
        if len(ob) == 28:
            # Walk-Jump or Walk-Jump-Crawl
            return ob[26] < 5.1
        elif len(ob) == 27:
            # Forward-Backward
            return ob[26] < 0