import React, { useState } from "react";
import { useTranslation, useLanguage } from "../../contexts/TranslationContext";
import { Language } from "../../types";

export interface LanguageOption {
  code: Language;
  name: string;
  nativeName: string;
  flag: string;
  dir: "ltr" | "rtl";
}

export interface LanguageSelectorProps {
  variant?: "dropdown" | "tabs" | "buttons";
  showFlag?: boolean;
  showNativeName?: boolean;
  size?: "sm" | "md" | "lg";
  className?: string;
  onLanguageChange?: (language: Language) => void;
}

const languageOptions: LanguageOption[] = [
  {
    code: "el",
    name: "Greek",
    nativeName: "Ελληνικά",
    flag: "🇬🇷",
    dir: "ltr",
  },
  {
    code: "en",
    name: "English",
    nativeName: "English",
    flag: "🇺🇸",
    dir: "ltr",
  },
];

export const LanguageSelector: React.FC<LanguageSelectorProps> = ({
  variant = "dropdown",
  showFlag = true,
  showNativeName = true,
  size = "md",
  className = "",
  onLanguageChange,
}) => {
  const { t } = useTranslation();
  const { language, setLanguage } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);

  const currentLanguage =
    languageOptions.find((lang) => lang.code === language) ||
    languageOptions[0];

  const handleLanguageChange = (newLanguage: Language) => {
    setLanguage(newLanguage);
    onLanguageChange?.(newLanguage);
    setIsOpen(false);
  };

  const sizeClasses = {
    sm: "text-sm px-2 py-1",
    md: "text-base px-3 py-2",
    lg: "text-lg px-4 py-3",
  };

  if (variant === "dropdown") {
    return (
      <div className={`relative ${className}`}>
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className={`
            flex items-center space-x-2 border border-gray-300 rounded-md 
            bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 
            focus:ring-blue-500 focus:border-blue-500 transition-colors
            ${sizeClasses[size]}
          `}
          aria-label={t("select_language")}
        >
          {showFlag && <span className="text-lg">{currentLanguage.flag}</span>}
          <span>
            {showNativeName ? currentLanguage.nativeName : currentLanguage.name}
          </span>
          <svg
            className={`w-4 h-4 transition-transform ${
              isOpen ? "rotate-180" : ""
            }`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        {isOpen && (
          <div className="absolute top-full left-0 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg z-50">
            {languageOptions.map((option) => (
              <button
                key={option.code}
                type="button"
                onClick={() => handleLanguageChange(option.code)}
                className={`
                  w-full flex items-center space-x-2 px-3 py-2 text-left
                  hover:bg-gray-50 focus:outline-none focus:bg-gray-50
                  ${option.code === language ? "bg-blue-50 text-blue-700" : ""}
                `}
              >
                {showFlag && <span className="text-lg">{option.flag}</span>}
                <div className="flex-1">
                  <div className="font-medium">
                    {showNativeName ? option.nativeName : option.name}
                  </div>
                  {showNativeName && option.nativeName !== option.name && (
                    <div className="text-xs text-gray-500">{option.name}</div>
                  )}
                </div>
                {option.code === language && (
                  <svg
                    className="w-4 h-4 text-blue-500"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                )}
              </button>
            ))}
          </div>
        )}
      </div>
    );
  }

  if (variant === "tabs") {
    return (
      <div className={`flex border-b border-gray-200 ${className}`}>
        {languageOptions.map((option) => (
          <button
            key={option.code}
            type="button"
            onClick={() => handleLanguageChange(option.code)}
            className={`
              flex items-center space-x-2 px-4 py-2 border-b-2 font-medium
              transition-colors focus:outline-none
              ${
                option.code === language
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }
              ${sizeClasses[size]}
            `}
          >
            {showFlag && <span className="text-lg">{option.flag}</span>}
            <span>{showNativeName ? option.nativeName : option.name}</span>
          </button>
        ))}
      </div>
    );
  }

  if (variant === "buttons") {
    return (
      <div className={`flex space-x-2 ${className}`}>
        {languageOptions.map((option) => (
          <button
            key={option.code}
            type="button"
            onClick={() => handleLanguageChange(option.code)}
            className={`
              flex items-center space-x-2 border rounded-md font-medium
              transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500
              ${
                option.code === language
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
              }
              ${sizeClasses[size]}
            `}
          >
            {showFlag && <span className="text-lg">{option.flag}</span>}
            <span>{showNativeName ? option.nativeName : option.name}</span>
          </button>
        ))}
      </div>
    );
  }

  return null;
};

export default LanguageSelector;
