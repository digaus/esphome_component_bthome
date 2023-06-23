/*
 Beethowen
 Beethowen over ESPNow virtual sensors for ESPHome

 Author: Attila Farago
 */

#pragma once

#include "esphome/core/component.h"

#include "esphome/components/bthome_receiver_base/bthome_receiver_base_hub.h"

namespace esphome
{
  namespace beethowen_receiver
  {
    class BeethowenReceiverHub : public esphome::bthome_receiver_base::BTHomeReceiverBaseHub
    {
    public:
      void setup() override;

    protected:
      void beethowen_on_data_(uint8_t *data, uint8_t size);
      void beethowen_on_command_(uint8_t command);
    };
  }
}