import numpy as np

from gym.envs.skills import BaseEnv

DEFAULT_CAMERA_CONFIG = {
    "trackbodyid": 2,
    "distance": 4.0,
    "lookat": np.array((0.0, 0.0, 1.15)),
    "elevation": -20.0,
}

class Walker2dEnv(BaseEnv):
    def __init__(self):
        # config
        self._config = {
            "random_steps": 0,
            "apply_force": 0,
            "prob_apply_force": 0,
            "ctrl_reward": 1e-3,
            "init_randomness": 0.01,
            "min_height": 0.8,
        }

        # env info
        self.reward_type = ["ctrl_reward"]
        self.ob_shape = {"joint": [17], "acc": [9]}
        self.ob_type = self.ob_shape.keys()

    def _ctrl_reward(self, a):
        ctrl_reward = -self._config["ctrl_reward"] * np.square(a).sum()
        return ctrl_reward

    def _get_walker2d_pos(self):
        return min(self.get_body_com("torso")[0],
                   self.get_body_com("foot")[0],
                   self.get_body_com("foot_left")[0])

    def get_ob_dict(self, ob):
        if len(ob.shape) > 1:
            return {'joint': ob[:, :17], 'acc': ob[:, 17:26]}
        else:
            return {'joint': ob[:17], 'acc': ob[17:26]}

    def viewer_setup(self):
        assert self.viewer is not None
        for key, value in DEFAULT_CAMERA_CONFIG.items():
            if isinstance(value, np.ndarray):
                getattr(self.viewer.cam, key)[:] = value
            else:
                setattr(self.viewer.cam, key, value)

    # methods to override for meta task classes:
    # ----------------------------
    def get_next_primitive(self, ob, prev_primitive):
        """ Return the next primitive. Implement this in each subclass.
        Returns:
            String of the primitive i.e. Walker2dJump-v1
        """
        raise NotImplementedError

    def is_terminate(self, ob, init=False, env=None):
        raise NotImplementedError