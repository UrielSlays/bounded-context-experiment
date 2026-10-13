"use strict";

const Ajv2020 = require("ajv/dist/2020").default;

module.exports.createAjv = function createAjv() {
  const ajv = new Ajv2020({
    strict: true,
    allErrors: true,
    validateFormats: true,
    allowUnionTypes: false,
  });
  ajv.addFormat("moonwalker-utc", {
    type: "string",
    validate(value) {
      const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{6})Z$/.exec(value);
      if (!match) return false;
      const [, yearText, monthText, dayText, hourText, minuteText, secondText] = match;
      const year = Number(yearText), month = Number(monthText), day = Number(dayText);
      const hour = Number(hourText), minute = Number(minuteText), second = Number(secondText);
      const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
      const monthDays = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
      return month >= 1 && month <= 12 && day >= 1 && day <= monthDays[month - 1]
        && hour <= 23 && minute <= 59 && second <= 59;
    },
  });
  return ajv;
};
