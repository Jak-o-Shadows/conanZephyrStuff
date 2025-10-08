/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

#include <hfsm2/machine.hpp>

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)

/*
 * A build error on this line means your board is unsupported.
 * See the sample documentation for information on how to fix this.
 */
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);


// Configure a simple state machine for the LED state
struct Context {
	unsigned delay_ms = 1000;
	unsigned count = 0;
	unsigned count_limit = 10;
};
using M = hfsm2::MachineT<hfsm2::Config::ContextT<Context>>;
#define S(s) struct s
using FSM = M::PeerRoot<
	           S(Fast),
			   S(Slow),
			   S(Medium)
			>;
#undef S

struct Fast: FSM::State {
	void enter(Control& control) {
		control.context().delay_ms = 100;
		control.context().count = 0;
		control.context().count_limit = 2000 / control.context().delay_ms;
	}
	void update(FullControl& control) {
		k_sleep(K_MSEC(control.context().delay_ms));
		control.context().count++;
		if (control.context().count >= control.context().count_limit) {
			control.changeTo<Medium>();
		}
	}
};
struct Medium: FSM::State {
	void enter(Control& control) {
		control.context().delay_ms = 500;
		control.context().count = 0;
		control.context().count_limit = 4000 / control.context().delay_ms;
	}
	void update(FullControl& control) {
		k_sleep(K_MSEC(control.context().delay_ms));
		control.context().count++;
		if (control.context().count >= control.context().count_limit) {
			control.changeTo<Slow>();
		}
	}
};
struct Slow: FSM::State {
	void enter(Control& control) {
		control.context().delay_ms = 2000;
		control.context().count = 0;
		control.context().count_limit = 5000 / control.context().delay_ms;
	}
	void update(FullControl& control) {
		k_sleep(K_MSEC(control.context().delay_ms));
		control.context().count++;
		if (control.context().count >= control.context().count_limit) {
			control.changeTo<Fast>();
		}
	}
};






extern "C"
int main()
{
	int ret;
	Context context;
	FSM::Instance machine{context};
	machine.changeTo<Fast>();
	machine.update();

	if (!gpio_is_ready_dt(&led)) {
		return 0;
	}

	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
	if (ret < 0) {
		return 0;
	}

	while (1) {
		ret = gpio_pin_toggle_dt(&led);
		if (ret < 0) {
			return 0;
		}

		machine.update();
	}
	return 0;
}
