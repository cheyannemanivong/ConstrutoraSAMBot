import constants as keys
from telegram import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import *
from datetime import datetime

print("Bot started.")

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
# ^ You can download your own credentials in JSON format after creating a new project in the Google Cloud Console.
# The Tech With Tim tutorial shows how to do this.
client = gspread.authorize(creds)
sheet = client.open("sheet name").sheet1  # in example_sheet.png, the sheet name is "tutorial"

vehicleNum = 0
# for "refueling procedure" conversation handler
VEHICLE, MILEAGE_BEFORE, MILEAGE_AFTER, QUANTITY, COST = range(5)
# for "driver" conversation handler
VEHICLE_DRIVER, NAME = range(2)
# for "license plate" conversation handler
VEHICLE_PLATE, PLATE = range(2)


def help_command(update, context):
    update.message.reply_text(keys.helpMenu)


def driver(update, context) -> int:
    reply_keyboard = [['1', '2', '3', '4']]  # 4 vehicles listed in the sheet

    update.message.reply_text(
        keys.driverString,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return VEHICLE_DRIVER


def select_vehicle_driver(update, context) -> int:
    # vehicle number
    global vehicleNum
    vehicleNum = int(update.message.text)

    update.message.reply_text(
        keys.selectVehicleDriverString1 +
        str(vehicleNum) +
        keys.selectVehicleDriverString2,
        reply_markup=ReplyKeyboardRemove()
    )

    return NAME


def name(update, context) -> int:
    # Enter name into google sheet
    sheet.update_cell(2, vehicleNum + 1, update.message.text)

    update.message.reply_text(keys.thankYou)

    return ConversationHandler.END


def plate(update, context) -> int:
    reply_keyboard = [['1', '2', '3', '4']]  # 4 vehicles listed in the sheet

    update.message.reply_text(
        keys.plateString,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return VEHICLE_PLATE


def select_vehicle_plate(update, context) -> int:
    # vehicle number
    global vehicleNum
    vehicleNum = int(update.message.text)

    update.message.reply_text(
        keys.selectVehiclePlateString1 +
        str(vehicleNum) +
        keys.selectVehiclePlateString2,
        reply_markup=ReplyKeyboardRemove()
    )

    return PLATE


def enter_plate(update, context) -> int:
    # Enter name into google sheet
    sheet.update_cell(3, vehicleNum + 1, update.message.text)

    update.message.reply_text(keys.thankYou)
    return ConversationHandler.END


def refuel(update, context) -> int:
    reply_keyboard = [['1', '2', '3', '4']]  # might need to change dynamically with the google sheet

    update.message.reply_text(
        keys.refuelString,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return VEHICLE


def select_vehicle_refuel(update, context) -> int:
    # vehicle number
    global vehicleNum
    vehicleNum = int(update.message.text)

    update.message.reply_text(
        keys.selectVehicleRefuelString1 +
        str(vehicleNum) +
        keys.selectVehicleRefuelString2,
        reply_markup=ReplyKeyboardRemove()
    )

    return MILEAGE_BEFORE


def mileage_before(update, context) -> int:
    # Enter mileage into google sheet
    sheet.update_cell(6, vehicleNum + 1, update.message.text)  # row 6 on sheet

    update.message.reply_text(keys.mileageBeforeString)

    return MILEAGE_AFTER


def mileage_after(update, context) -> int:
    # Enter mileage into google sheet
    sheet.update_cell(7, vehicleNum + 1, update.message.text)

    update.message.reply_text(keys.mileageAfterString)

    return QUANTITY


def refuel_quantity(update, context) -> int:
    # Enter quantity into google sheet
    sheet.update_cell(8, vehicleNum + 1, update.message.text)

    update.message.reply_text(keys.refuelQuantityString)

    return COST


def refuel_cost(update, context) -> int:
    # Enter cost and date into google sheet
    sheet.update_cell(9, vehicleNum + 1, update.message.text)
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
    sheet.update_cell(5, vehicleNum + 1, date)

    update.message.reply_text(keys.refuelCostString)

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(keys.commandStopped, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help_command))

    # Add refueling conversation handler with the states VEHICLE, MILEAGE_BEFORE, MILEAGE_AFTER, QUANTITY, COST
    refueling_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('refuel', refuel)],
        states={
            VEHICLE: [MessageHandler(Filters.regex('^(1|2|3|4)$'), select_vehicle_refuel)],
            MILEAGE_BEFORE: [MessageHandler(Filters.text & ~Filters.command, mileage_before)],
            MILEAGE_AFTER: [MessageHandler(Filters.text & ~Filters.command, mileage_after)],
            QUANTITY: [MessageHandler(Filters.text & ~Filters.command, refuel_quantity)],
            COST: [MessageHandler(Filters.text & ~Filters.command, refuel_cost)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(refueling_conv_handler)

    # Add driver conversation handler with the states VEHICLE_DRIVER, NAME
    driver_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('driver', driver)],
        states={
            VEHICLE_DRIVER: [MessageHandler(Filters.regex('^(1|2|3|4)$'), select_vehicle_driver)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(driver_conv_handler)

    # Add license plate conversation handler with the states VEHICLE_PLATE, PLATE
    plate_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('plate', plate)],
        states={
            VEHICLE_PLATE: [MessageHandler(Filters.regex('^(1|2|3|4)$'), select_vehicle_plate)],
            PLATE: [MessageHandler(Filters.text & ~Filters.command, enter_plate)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(plate_conv_handler)

    updater.start_polling()
    updater.idle()


main()
