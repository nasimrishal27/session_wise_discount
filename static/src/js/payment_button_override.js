/** @odoo-module **/
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";


patch(PaymentScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    async validateOrder(isForceValidate) {
        const order = this.pos.get_order();
        const session = this.pos.config.current_session_id;
        const session_discount_limit = session?.session_discount_limit ?? 0;

        let totalLineDiscount = 0;
        let totalGlobalDiscount = 0;

        const discountProductId = this.pos.config.discount_product_id?.id;
        console.log(this.pos.config.discount_product_id)
        console.log(discountProductId)

        order.get_orderlines().forEach(line => {
            if (line.product_id?.id === discountProductId) {
                totalGlobalDiscount += Math.abs(line.get_price_with_tax());
            } else {
                const unitPrice = line.get_unit_price();
                const discount = line.get_discount();
                const quantity = line.get_quantity();

                totalLineDiscount += (unitPrice * discount / 100) * quantity;
            }
        });

        const totalDiscount = totalLineDiscount + totalGlobalDiscount;
        console.log(totalLineDiscount)
        console.log(totalGlobalDiscount)
        console.log(totalDiscount)
        console.log(session_discount_limit)

        if (totalDiscount > session_discount_limit || session_discount_limit <= 0) {
            await this.notification.add(_t("Session discount limit exceeded."), {
                title: "Validation Error",
                type: "warning"
            });
            return;
        }

        await rpc("/pos/update_session_discount_limit", {
            session_id: session.id,
            used_discount: totalDiscount
        });

        return super.validateOrder(isForceValidate);
    }
});

